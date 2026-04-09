# StudyAI — Full Stack Flask App

AI-powered study assistant. Upload PDFs, generate summaries, quizzes & flashcards.

## Setup

```bash
pip install flask werkzeug pdfplumber
python app.py
# → http://localhost:5000
```

## Demo Login
- Email: `demo@studyai.com`
- Password: `demo123`

## Features
- **Login / Register** — session-based auth with password hashing
- **Upload PDF** — drag & drop, up to 16MB
- **PDF Summarizer** — structured AI summary via Claude API
- **Quiz Generator** — 5/8/10 MCQ with scoring & explanations
- **Flashcards** — flip cards + grid view, keyboard navigation

## API Key Required
AI features need an Anthropic API key from https://console.anthropic.com
Enter it per-session in each tool page (stored in memory only).

## Stack
- **Backend**: Flask + Werkzeug + pdfplumber
- **AI**: Anthropic Claude via REST API
- **Frontend**: Vanilla JS + CSS (no JS framework needed)
- **Auth**: Flask session + Werkzeug password hashing
- **Storage**: In-memory (swap with MySQL for production)

## Production Notes
- Replace `users_db` and `materials_db` with MySQL
- Move `secret_key` to environment variable
- Use a proper file storage (S3/MinIO) for uploads
- Add rate limiting on API endpoints
