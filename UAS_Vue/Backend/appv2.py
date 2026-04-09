import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

uhost = "localhost"
uuser = "root"
upassword = "FNDDatabase.1"
ucarset = "utf8mb4"
udatabase = "tugasdb"

def initialize_db():
    conn = pymysql.connect(
        host=uhost,
        user=uuser,
        password=upassword,
        charset=ucarset,
        cursorclass=pymysql.cursors.Cursor
    )
    cursor = conn.cursor()
    # cursor.execute("DROP DATABASE IF EXISTS tugasdb")
    cursor.execute("CREATE DATABASE IF NOT EXISTS tugasdb")
    cursor.execute("USE tugasdb")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INT AUTO_INCREMENT PRIMARY KEY,
            hari ENUM('Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'),
            judul VARCHAR(255),
            date DATE,
            Kategori ENUM('Important', 'Urgent', 'Reguler', 'Done'),
            deskripsi TEXT,
            status ENUM('Active', 'Deleted','Done') DEFAULT 'Active'
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM task")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO task (hari, judul, date, Kategori, deskripsi)
            VALUES (%s, %s, %s, %s, %s)
        ''', [
            ("Senin", "Belajar Flask", "2025-05-05", "Important", "Membuat API Flask dasar"),
            ("Selasa", "Vue Integration", "2025-05-06", "Urgent", "Hubungkan Vue dengan Flask"),
            ("Rabu", "Database Review", "2025-05-07", "Reguler", "Tinjau ERD dan relasi antar tabel"),
            ("Kamis", "Uji Coba API", "2025-05-08", "Important", "Tes GET, PUT, POST endpoint"),
            ("Jumat", "Deploy ke Render", "2025-05-09", "Urgent", "Hosting Flask + Vue ke internet")
        ])
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if username == "admin" and password == "abcdef":
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/api", methods=["GET"])
def get_tasks():
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM task")
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(tasks), 200

@app.route("/api", methods=["POST"])
def create_task():
    task = request.get_json()
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    sql = "INSERT INTO task (hari, judul, date, Kategori, deskripsi) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (
        task["hari"], task["judul"], task["date"],
        task["Kategori"], task["deskripsi"]
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Task created"}), 201

@app.route("/api/<int:task_id>", methods=["GET"])
def get_task(task_id):
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM task WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    if task:
        return jsonify(task), 200
    return jsonify({"message": "Task not found"}), 404

@app.route("/api/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = request.get_json()
    try:
        conn = pymysql.connect(
            host=uhost, user=uuser, password=upassword, database=udatabase,
            charset=ucarset, cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        sql = "UPDATE task SET hari = %s, judul = %s, date = %s, Kategori = %s, deskripsi = %s WHERE id = %s"
        cursor.execute(sql, (
            task["hari"], task["judul"], task["date"],
            task["Kategori"], task["deskripsi"], task_id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Task updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE task SET status = 'Deleted' WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Task deleted"}), 200

@app.route("/api/<int:task_id>/done", methods=["PUT"])
def mark_task_done(task_id):
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("UPDATE task SET status = 'Done', Kategori = 'Done' WHERE id = %s", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Task marked as Done"}), 200

if __name__ == "__main__":
    initialize_db()
    app.run(debug=True)
