from flask import Flask, jsonify, request
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Konfigurasi Database
db_config = {
    'user': 'root',
    'password': 'FNDDatabase.1', # Isi password database Anda
    'host': 'localhost',
    'database': 'taskInventory_db',
    'port': 3306
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
    cursor.execute("DROP DATABASE IF EXISTS taskInventory_db")
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
    ('Tugas Paper', 'Membuat Paper mengenai analisa kemunduran demokrasi', 'U', NOW()),
    ('Belajar CTF', 'Mempelajari SQL Injection','I', NOW()),
    ('Mengubah sistem laptop lama menjadi Linux', 'Linux', 'N', NOW())
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


@app.route('/api/tasks/add', methods=['POST'])
def add_task():
    try:
        # Ambil data dari request JSON
        data = request.get_json()
        
        # Validasi data
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        # Validasi field required
        if 'title' not in data or not data['title'].strip():
            return jsonify({
                'success': False,
                'message': 'Title is required'
            }), 400
        
        # Ambil data dari request
        title = data['title'].strip()
        description = data.get('description', '').strip()
        category = data.get('category', 'N')  # Default 'N' (Normal)
        status = data.get('status', 'New')  # Default 'New'
        created_time = datetime.now()
        
        # Validasi category
        valid_categories = ['N', 'U', 'I']
        if category not in valid_categories:
            return jsonify({
                'success': False,
                'message': f'Invalid category. Must be one of: {", ".join(valid_categories)}'
            }), 400
        
        # Validasi status
        valid_statuses = ['New', 'In Progress', 'Done']
        if status not in valid_statuses:
            return jsonify({
                'success': False,
                'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
            }), 400
        
        # Insert ke database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql_query = """
            INSERT INTO tasks (title, description, category, status, created_time, deleted) 
            VALUES (%s, %s, %s, %s, %s, 'False')
        """
        values = (title, description, category, status, created_time)
        
        cursor.execute(sql_query, values)
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task added successfully',
        }), 201
        
    except mysql.connector.Error as e:
        return jsonify({
            'success': False,
            'message': f'Database error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

    
if __name__ == '__main__':
    createdb()
    app.run(host='0.0.0.0', port=5000, debug=True)