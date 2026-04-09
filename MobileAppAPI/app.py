from flask import Flask, jsonify, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Konfigurasi Database
db_config = {
    'user': 'root',
    'password': 'FNDDatabase.1', # Isi password database Anda
    'host': 'localhost',
    'database': 'taskInventory_db'
    
   
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

def get_db_connection_no_db():
    config_no_db = db_config.copy()
    config_no_db.pop('database', None)
    return mysql.connector.connect(**config_no_db)

def createdb():
    conn = get_db_connection_no_db()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS taskInventory_db")
    cursor.execute("USE taskInventory_db")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    description Text,
    category ENUM('N', 'U','I') DEFAULT 'N',
    status ENUM('New', 'In Progress','Done') DEFAULT 'New',
    created_time datetime,
    finished_time datetime,
    duration int,
    deleted ENUM('False', 'True') DEFAULT 'False'
    )""")

    cursor.execute("""
    INSERT INTO tasks (title, description, category, created_time) VALUES 
    ('Tugas UAS Mobile App', 'Buat Aplikasi Task Inventory', 'U', NOW()),
    ('Tugas Paper', 'Membuat Paper mengenai analisa kemunduran demokrasi', 'U', NOW())
    """)

    conn.commit()
    cursor.close()
    conn.close()


@app.route('/api/tasks', methods=['GET'])
def get_task():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks")
    movies = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(movies)

# @app.route('/api/tasks', methods=['POST'])
# def add_task():
#     data = request.json
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     current_datetime = datetime.now()

#     query = "INSERT INTO tasks (title, description, category, created_time) VALUES (%s, %s, %s, %s)"
#     values = (data['title'], data['description'], data['category'], current_datetime)
    
#     cursor.execute(query, values)
#     conn.commit()
    
#     cursor.close()
#     conn.close()
#     return jsonify({"message": "Add Task Success!", "status": 200})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task_status(task_id):
    new_status = request.form.get('status') 
    conn = get_db_connection()
    cursor = conn.cursor()
    if new_status == 'Done':
        finished_time = datetime.now()
        sql_query = "UPDATE tasks SET status = %s, finished_time = %s, duration = TIMESTAMPDIFF(MINUTE, created_time, %s) WHERE id = %s"
        values = (new_status, finished_time, finished_time, task_id)
    else:
        sql_query = "UPDATE tasks SET status = %s WHERE id = %s"
        values = (new_status, task_id)

    cursor.execute(sql_query, values)
    conn.commit()

    if cursor.rowcount == 0:
        return jsonify({'message': 'Task ID tidak ditemukan'}), 404

    cursor.close()
    conn.close()


    return jsonify({'message': 'Status berhasil diupdate'}), 200

@app.route('/api/tasks', methods=['POST'])
def create_task():
    try:
        # 1. Ambil data dari Android
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category') # Isinya 'N', 'U', atau 'I'

        # Validasi
        if not title:
            return jsonify({'message': 'Judul tidak boleh kosong'}), 400

        # 2. Siapkan Data Default
        status = 'New'
        created_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        deleted = 'False'

        # 3. Query Insert ke MySQL
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO tasks (title, description, category, status, created_time, deleted) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        val = (title, description, category, status, created_time, deleted)
        
        cursor.execute(sql, val)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Task berhasil dibuat!'}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Gagal menyimpan data'}), 500
    
if __name__ == '__main__':
    # createdb()
    app.run(host='0.0.0.0', port=5000, debug=True)