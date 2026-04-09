import logging
import sqlite3
from flask import Flask, request, render_template_string

# --- KONFIGURASI LOG ---
log_file_path = r'C:\logs\serangan.log'

logging.basicConfig(
    filename=log_file_path, 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
# -----------------------

app = Flask(__name__)

# Fungsi untuk menyiapkan Database Dummy (SQLite)
# Kita buat tabel user sederhana di memori (RAM)
def get_db_connection():
    conn = sqlite3.connect(':memory:') # Database di RAM, hilang saat restart
    cursor = conn.cursor()
    # Buat tabel
    cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    # Masukkan user admin asli
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
    conn.commit()
    return conn

# HTML Template (Tetap sama)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Vulnerable Bank Login</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5; }
        .login-container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-top: 5px solid red; }
        input { display: block; margin: 10px 0; padding: 10px; width: 100%; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer; }
        .error { color: red; margin-bottom: 10px; }
        .info { font-size: 12px; color: #666; margin-top: 10px; text-align: center; }
    </style>
</head>
<body>
    <div class="login-container">
        <h2 style="color: #dc3545;">Login (Vulnerable)</h2>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
        <form method="post">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="info">System: SQLite3 (In-Memory)</div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip_address = request.remote_addr
        
        # 1. Koneksi ke Database
        conn = get_db_connection()
        cursor = conn.cursor()

        # --- BAGIAN VULNERABLE (SQL INJECTION) ---
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        print(f"[DEBUG] Query SQL yang dieksekusi: {query}") # Untuk melihat bentuk query di terminal
        
        try:
            # Eksekusi query jahat
            cursor.execute(query)
            user = cursor.fetchone()
            
            if user:
                # Jika SQL mengembalikan hasil (berarti login sukses atau ter-bypass)
                log_msg = f"CustomApp: LOGIN_SUCCESS User '{username}' (Query: {query}) from IP {ip_address}"
                logging.info(log_msg)
                print(f"[+] {log_msg}")
                return f"<h1>Login BERHASIL!</h1><p>Welcome, user ID: {user[0]}</p><p>Query executed: {query}</p>"
            else:
                # Login Gagal
                log_msg = f"CustomApp: LOGIN_FAILED User '{username}' (Query: {query}) from IP {ip_address}"
                logging.info(log_msg)
                print(f"[-] {log_msg}")
                error = "Username atau Password Salah!"
                
        except Exception as e:
            # Jika injection merusak syntax SQL (Error SQL)
            log_msg = f"CustomApp: SQL_ERROR '{e}' from IP {ip_address}"
            logging.info(log_msg)
            error = f"Database Error: {e}"
        finally:
            conn.close()

    return render_template_string(HTML_TEMPLATE, error=error)

if __name__ == '__main__':
    print(f"[*] Aplikasi VULNERABLE berjalan.")
    print(f"[*] Log file: {log_file_path}")
    app.run(host='0.0.0.0', port=5000)