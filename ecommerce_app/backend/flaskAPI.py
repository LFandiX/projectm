import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

uhost = "localhost"
uuser = "root"
upassword = "FNDDatabase.1"
ucarset = "utf8mb4"
udatabase = "ecommerce_dbs"

def initialize_db():
    conn = pymysql.connect(
        host=uhost,
        user=uuser,
        password=upassword,
        charset=ucarset,
        cursorclass=pymysql.cursors.Cursor
    )
    cursor = conn.cursor()
    # cursor.execute("DROP DATABASE IF EXISTS ecommerce_dbs")
    cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce_dbs")
    cursor.execute("USE ecommerce_dbs")
# Create products table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            stock INT DEFAULT 0,
            image_url VARCHAR(255) DEFAULT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS basket (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            kelas varchar(255) NOT NULL,
            quantity INT DEFAULT 1 NOT NULL,
            total_price DECIMAL(10, 2) NOT NULL,
            note TEXT,
            status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
            payment_method ENUM('Tunai', 'Transfer') NOT NULL,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            voucher_id INT DEFAULT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vouchers (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            discount DECIMAL(10, 2) NOT NULL,
            code VARCHAR(50) NOT NULL UNIQUE,
            expiration_date TIMESTAMP NOT NULL
        )
    """)    
    conn.commit()
    cursor.close()
    conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (data.get("username"), data.get("password")))
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({"message": "Invalid credentials"}), 401
    else:
        user = cursor.fetchone()
        cursor.execute("SELECT * FROM basket WHERE id = %s", (user['id'],))
        basket = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({"message": "Login successful", "user": user, "basket": basket}), 200
    
@app.route("/users", methods=["get"])
def get_users():
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users), 200

@app.route("/createusers", methods=["POST"])
def create_user():
    data = request.get_json()
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                   (data.get("name"), data.get("email"), data.get("password")))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User created successfully"}), 201

@app.route("/products", methods=["get"])
def get_products():
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(products), 200

@app.route("/basket/<int:user_id>", methods=["GET"])
def get_basket(user_id):
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT b.id, b.product_id, b.user_id, b.quantity, p.nama, p.image FROM basket b JOIN products p ON b.product_id = p.id WHERE b.user_id = %s;", (user_id,))
    basket = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(basket), 200
    

@app.route("/basket", methods=["POST"])
def add_to_basket():
    data = request.get_json()
    
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO basket (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                   (data.get("user_id"), data.get("product_id"), data.get("quantity")))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Item added to basket"}), 201

@app.route("/getbasket/<int:user_id>", methods=["GET"])
def get_basket_items(user_id):
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM basket WHERE user_id = %s", (user_id,))
    basket_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(basket_items), 200

@app.route("/basket/<int:id>", methods=["DELETE"])
def delete_basket_item(id):
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM basket WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Basket item deleted"}), 200

@app.route("/history", methods=["POST"])
def add_history():
    data = request.get_json()
    
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (user_id, product_id, kelas, quantity, total_price, note, payment_method, voucher_id) VALUES (%s, %s, %s, %s, %s, %s,%s, %s)",
                   (data.get("user_id"), data.get("product_id"), data.get("kelas"), data.get("quantity"),data.get("total_price"),data.get("note"), data.get("payment_method"),data.get("voucher_id")))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Item Purchased!, Waiting for Payment"}), 201

@app.route("/gethistory/<int:user_id>", methods=["GET"])
def get_history_items(user_id):
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM history WHERE user_id = %s", (user_id,))
    basket_items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(basket_items), 200

@app.route("/history/<int:user_id>", methods=["GET"])
def get_history(user_id):
    conn = pymysql.connect(
        host=uhost, user=uuser, password=upassword, database=udatabase,
        charset=ucarset, cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    cursor.execute("SELECT b.id, b.product_id, b.total_price,b.status, b.quantity,b.payment_method,b.purchase_date, p.nama, p.image FROM history b JOIN products p ON b.product_id = p.id WHERE b.user_id = %s;", (user_id,))
    basket = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(basket), 200


from flask import send_from_directory

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/image/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
