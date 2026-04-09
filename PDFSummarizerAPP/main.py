from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os, json, uuid, pdfplumber, re, urllib.request, urllib.error

app = Flask(__name__)
app.secret_key = 'studyai-dev-secret-2024'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

# ── In-memory stores ──────────────────────────────────────────────────────────
users_db = {
    "demo@studyai.com": {
        "name": "Alex Johnson",
        "password": generate_password_hash("demo123"),
        "avatar": "AJ",
        "plan": "Pro",
    }
}

# { user_email: [ {id, filename, original_name, text, summary, quiz, flashcards, uploaded_at} ] }
materials_db = {}

# ── Helpers ───────────────────────────────────────────────────────────────────
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_pdf_text(filepath):
    text = []
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text.append(t)
    return '\n'.join(text)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_user_materials():
    return materials_db.get(session.get('user_email'), [])

def get_material_by_id(mid):
    for m in get_user_materials():
        if m['id'] == mid:
            return m
    return None

# ── Gemini API helper ─────────────────────────────────────────────────────────
def call_gemini(api_key, prompt, max_tokens=2048):
    """Call Gemini 2.0 Flash (free tier) and return the text response."""
    import json as _json
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    payload = _json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": max_tokens,
            "temperature": 0.4
        }
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = _json.loads(resp.read())
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if e.code == 400:
            raise Exception(f"Bad request: {body}")
        if e.code == 403:
            raise Exception("Invalid or unauthorized API key. Check your Gemini key.")
        raise Exception(f"HTTP {e.code}: {body}")


# ── Auth routes ───────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('dashboard') if 'user_email' in session else url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_email' in session:
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        user = users_db.get(email)
        if user and check_password_hash(user['password'], password):
            session.update({'user_email': email, 'user_name': user['name'],
                            'user_avatar': user['avatar'], 'user_plan': user['plan']})
            return redirect(url_for('dashboard'))
        error = "Invalid email or password."
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        name  = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        pwd   = request.form.get('password', '')
        cpwd  = request.form.get('confirm_password', '')
        if not name or not email or not pwd:
            error = "All fields are required."
        elif pwd != cpwd:
            error = "Passwords do not match."
        elif len(pwd) < 6:
            error = "Password must be at least 6 characters."
        elif email in users_db:
            error = "Email already registered."
        else:
            initials = ''.join([w[0].upper() for w in name.split()[:2]])
            users_db[email] = {"name": name, "password": generate_password_hash(pwd),
                                "avatar": initials, "plan": "Free"}
            session.update({'user_email': email, 'user_name': name,
                            'user_avatar': initials, 'user_plan': "Free"})
            return redirect(url_for('dashboard'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── Dashboard ─────────────────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    mats = get_user_materials()
    stats = {
        'uploads':    len(mats),
        'summaries':  sum(1 for m in mats if m.get('summary')),
        'quizzes':    sum(len(m.get('quiz', [])) for m in mats),
        'flashcards': sum(len(m.get('flashcards', [])) for m in mats),
    }
    return render_template('dashboard.html',
        user_name=session['user_name'], user_avatar=session['user_avatar'],
        user_plan=session['user_plan'], stats=stats, materials=mats[:5])

# ── Upload ────────────────────────────────────────────────────────────────────
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    filename  = secure_filename(file.filename)
    uid       = str(uuid.uuid4())[:8]
    safe_name = f"{uid}_{filename}"
    filepath  = os.path.join(app.config['UPLOAD_FOLDER'], safe_name)
    file.save(filepath)

    try:
        text = extract_pdf_text(filepath)
    except Exception as e:
        return jsonify({'error': f'Could not read PDF: {str(e)}'}), 500

    if not text.strip():
        return jsonify({'error': 'PDF appears to be empty or image-only'}), 400

    material = {
        'id': uid, 'filename': safe_name, 'original_name': filename,
        'text': text, 'summary': None, 'quiz': [], 'flashcards': [],
        'uploaded_at': __import__('datetime').datetime.now().strftime('%b %d, %Y'),
        'word_count': len(text.split()),
        'pages': text.count('\f') + 1,
    }
    email = session['user_email']
    if email not in materials_db:
        materials_db[email] = []
    materials_db[email].insert(0, material)

    return jsonify({'success': True, 'id': uid, 'name': filename,
                    'word_count': material['word_count']})

# ── Materials list ─────────────────────────────────────────────────────────────
@app.route('/materials')
@login_required
def materials():
    return render_template('materials.html',
        user_name=session['user_name'], user_avatar=session['user_avatar'],
        user_plan=session['user_plan'], materials=get_user_materials())

# ── Summarizer ─────────────────────────────────────────────────────────────────
@app.route('/summarizer')
@login_required
def summarizer():
    mid  = request.args.get('id')
    mat  = get_material_by_id(mid) if mid else None
    mats = get_user_materials()
    return render_template('summarizer.html',
        user_name=session['user_name'], user_avatar=session['user_avatar'],
        user_plan=session['user_plan'], material=mat, materials=mats)

@app.route('/api/summarize', methods=['POST'])
@login_required
def api_summarize():
    data    = request.get_json()
    mid     = data.get('id')
    api_key = data.get('api_key', '').strip()
    mat     = get_material_by_id(mid)
    if not mat:
        return jsonify({'error': 'Material not found'}), 404
    if not api_key:
        return jsonify({'error': 'API key required'}), 400

    text = mat['text'][:12000]
    prompt = f"""Summarize the following study material clearly and concisely.
Structure your response with:
1. **Overview** (2-3 sentences)
2. **Key Concepts** (bullet points)
3. **Important Details** (bullet points)
4. **Takeaways** (2-3 sentences)

Material:
{text}"""

    try:
        summary = call_gemini(api_key, prompt, max_tokens=1500)
        mat['summary'] = summary
        return jsonify({'summary': summary})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── Quiz Generator ─────────────────────────────────────────────────────────────
@app.route('/quiz')
@login_required
def quiz():
    mid  = request.args.get('id')
    mat  = get_material_by_id(mid) if mid else None
    mats = get_user_materials()
    return render_template('quiz.html',
        user_name=session['user_name'], user_avatar=session['user_avatar'],
        user_plan=session['user_plan'], material=mat, materials=mats)

@app.route('/api/generate-quiz', methods=['POST'])
@login_required
def api_generate_quiz():
    data    = request.get_json()
    mid     = data.get('id')
    api_key = data.get('api_key', '').strip()
    count   = min(int(data.get('count', 5)), 10)
    mat     = get_material_by_id(mid)
    if not mat:
        return jsonify({'error': 'Material not found'}), 404
    if not api_key:
        return jsonify({'error': 'API key required'}), 400

    text = mat['text'][:10000]
    prompt = f"""Generate exactly {count} multiple-choice quiz questions from the study material below.

Respond ONLY with a valid JSON array. No extra text, no markdown fences, no explanation.
Format:
[
  {{
    "question": "Question text?",
    "options": ["A. option", "B. option", "C. option", "D. option"],
    "answer": "A",
    "explanation": "Brief explanation why this is correct."
  }}
]

Material:
{text}"""

    try:
        import json as _json
        raw = call_gemini(api_key, prompt, max_tokens=2000).strip()
        raw = re.sub(r'^```(?:json)?\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)
        questions = _json.loads(raw)
        mat['quiz'] = questions
        return jsonify({'questions': questions})
    except _json.JSONDecodeError:
        return jsonify({'error': 'AI returned invalid format. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ── Flashcards ─────────────────────────────────────────────────────────────────
@app.route('/flashcards')
@login_required
def flashcards():
    mid  = request.args.get('id')
    mat  = get_material_by_id(mid) if mid else None
    mats = get_user_materials()
    return render_template('flashcards.html',
        user_name=session['user_name'], user_avatar=session['user_avatar'],
        user_plan=session['user_plan'], material=mat, materials=mats)

@app.route('/api/generate-flashcards', methods=['POST'])
@login_required
def api_generate_flashcards():
    data    = request.get_json()
    mid     = data.get('id')
    api_key = data.get('api_key', '').strip()
    count   = min(int(data.get('count', 8)), 20)
    mat     = get_material_by_id(mid)
    if not mat:
        return jsonify({'error': 'Material not found'}), 404
    if not api_key:
        return jsonify({'error': 'API key required'}), 400

    text = mat['text'][:10000]
    prompt = f"""Generate exactly {count} flashcards from the study material below.

Respond ONLY with a valid JSON array. No extra text, no markdown fences.
Format:
[
  {{"front": "Term or question", "back": "Definition or answer"}}
]

Material:
{text}"""

    try:
        import json as _json
        raw = call_gemini(api_key, prompt, max_tokens=1500).strip()
        raw = re.sub(r'^```(?:json)?\s*', '', raw)
        raw = re.sub(r'\s*```$', '', raw)
        cards = _json.loads(raw)
        mat['flashcards'] = cards
        return jsonify({'flashcards': cards})
    except _json.JSONDecodeError:
        return jsonify({'error': 'AI returned invalid format. Please try again.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)