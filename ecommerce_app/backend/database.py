import mysql.connector

def create_database():
    """Create the MySQL database and tables if they do not exist."""
    connection = get_db_connection()
    if connection is None:
        return

    cursor = connection.cursor()
    try:
        cursor.execute("DROP DATABASE ecommerce_dbs")
        cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce_dbs")
        cursor.execute("USE ecommerce_dbs")
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(255) NOT NULL,
                deskripsi TEXT,
                harga INT NOT NULL,
                stock INT DEFAULT 0,
                status ENUM('Publish', 'Unpublish') DEFAULT 'Publish',
                image VARCHAR(255) DEFAULT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'user') DEFAULT 'user',
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
        # cursor.execute("""
        #     INSERT INTO users (name, email, password)
        #     VALUES ('John Doe', 'john@example.com', 'password123'), ('Osis Merch', 'osismerchandise@gmail.com', 'admin123')
        # """)
        
        
        print("Database and tables created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating database or tables: {err}")
    finally:
        cursor.close()
        close_db_connection(connection)

def get_db_connection():
    """Establish a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='FNDDatabase.1',
            database='ecommerce_dbs'
            
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def close_db_connection(connection):
    """Close the database connection."""
    if connection:
        try:
            connection.close()
            print("Database connection closed.")
        except mysql.connector.Error as err:
            print(f"Error closing connection: {err}")
    else:
        print("No connection to close.")    

def get_user():
    """Fetch all users from the database."""
    connection = get_db_connection()
    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", ('john@example.com', 'password123'))
        users = cursor.fetchall()
        return users
    except mysql.connector.Error as err:
        print(f"Error fetching users: {err}")
        return []
    finally:
        cursor.close()
        close_db_connection(connection)


if __name__ == "__main__":
    create_database()
    # Uncomment the following lines to test fetching users
#    users = get_user()
#    print(users[0]['name'])

