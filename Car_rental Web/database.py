import mysql.connector

# Koneksi ke database
def connect_db():
    return mysql.connector.connect(
        host="alfandi-db.cluster-cdm4ewgaio3j.us-east-1.rds.amazonaws.com",
        user="admin",
        password="FNDDatabase.1",
        database="rental_mobil"
    )

# Membuat database dan tabel jika belum ada
def setup_database():
    conn = mysql.connector.connect(host="alfandi-db.cluster-cdm4ewgaio3j.us-east-1.rds.amazonaws.com", user="admin", password="FNDDatabase.1")
    cursor = conn.cursor()
    # cursor.execute("Drop DATABASE rental_mobil")
    cursor.execute("CREATE DATABASE IF NOT EXISTS rental_mobil")
    conn.database = "rental_mobil"

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('Customer', 'Admin') NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INT AUTO_INCREMENT PRIMARY KEY,
            brand VARCHAR(100) NOT NULL,
            model VARCHAR(100) NOT NULL,
            description TEXT,
            year INT NOT NULL,
            price_per_day DECIMAL(10,2) NOT NULL,
            status ENUM('Available', 'Rented') DEFAULT 'Available',
            seats INT NOT NULL,
            mode ENUM('Manual', 'Automatic') NOT NULL,
            fuel ENUM('Petrol', 'Diesel', 'Electric') NOT NULL,
            image_link TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            car_id INT,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            status ENUM('Waiting For Approval', 'Ongoing', 'Completed') DEFAULT 'Waiting For Approval',
            total_days INT GENERATED ALWAYS AS (DATEDIFF(end_date, start_date)),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (car_id) REFERENCES cars(id)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Fungsi register user
def register_user(username, password, role):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                   (username, password, role))
    conn.commit()
    cursor.close()
    conn.close()


# Fungsi menambahkan mobil
def add_car(brand, model,description, year, price_per_day,seats,mode,fuel,image_link):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cars (brand, model, description, year, price_per_day,status,seats,mode,fuel,image_link) VALUES (%s, %s ,%s, %s, %s,%s, %s, %s, %s, %s)", 
                   (brand, model,description, year, price_per_day,'Available',seats,mode,fuel,image_link))
    conn.commit()
    cursor.close()
    conn.close()


# Fungsi untuk menerima rental mobil
def rent_car(user_id, car_id, start_date, end_date):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Cek apakah mobil tersedia
    cursor.execute("SELECT status, price_per_day FROM cars WHERE id = %s", (car_id,))
    car = cursor.fetchone()
    if not car or car[0] == 'Rented':
        print("Car is not available!")
        return

    # Hitung total harga
    price_per_day = car[1]
    days = (end_date - start_date).days
    total_price = days * price_per_day

    # Insert rental
    cursor.execute("INSERT INTO rentals (user_id, car_id, start_date, end_date, total_price) VALUES (%s, %s, %s, %s, %s)", 
                   (user_id, car_id, start_date, end_date, total_price))
    
    # Update status mobil
    
    conn.commit()
    cursor.close()
    conn.close()


# Fungsi untuk melihat history rental customer
def customer_history(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, c.brand, c.model, r.start_date, r.end_date, r.total_price, r.status, r.total_days, DATEDIFF(r.end_date, CURDATE()) as days_remaining,c.image_link
        FROM rentals r
        JOIN cars c ON r.car_id = c.id
        WHERE r.user_id = %s
    """, (user_id,))
    
    data =  cursor.fetchall()
       
    
    cursor.close()
    conn.close()
    return data

# Fungsi untuk melihat seluruh history rental (Admin)
def admin_history():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, c.brand, c.model, r.start_date, r.end_date, r.total_price, r.status, r.total_days, DATEDIFF(r.end_date, CURDATE()) as days_remaining, c.image_link, u.username
        FROM rentals r
        JOIN users u ON r.user_id = u.id
        JOIN cars c ON r.car_id = c.id
    """)
    
    data =  cursor.fetchall()
       
    
    cursor.close()
    conn.close()
    return data

# Fungsi menyelesaikan rental
def complete_rental(rental_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Ambil ID mobil terkait
    cursor.execute("SELECT car_id FROM rentals WHERE id = %s", (rental_id,))
    car_id = cursor.fetchone()
    
    if not car_id:
        print("Rental not found!")
        return
    
    car_id = car_id[0]

    # Update status rental menjadi 'Completed'
    cursor.execute("UPDATE rentals SET status = 'Completed' WHERE id = %s", (rental_id,))
    
    # Update status mobil menjadi 'Available'
    cursor.execute("UPDATE cars SET status = 'Available' WHERE id = %s", (car_id,))
    
    conn.commit()
    cursor.close()
    conn.close()

def show_cars():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def admin_approve(user_id, car_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE rentals SET status = 'Ongoing' WHERE user_id = %s AND car_id = %s", (user_id, car_id))
    cursor.execute("UPDATE cars SET status = 'Rented' WHERE id = %s", (car_id,))
    conn.commit()

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


if __name__ == "__main__":
    import datetime
    
    setup_database()
    register_user("admin", "adminpass", "Admin")
    register_user("user1", "password123", "Customer")
    register_user("user2", "password123", "Customer")

    register_user("user3", "password123", "Customer")

    register_user("user4", "password123", "Customer")

    register_user("user5", "password123", "Customer")

    add_car("Toyota", "Agya", "Hatchback ekonomis dengan desain sporty.", 2022, 250000, 5, "Automatic", "Petrol", "images/agya/TRAC_City_Car_Toyota_Agya_3089af640d.webp")
    add_car("Daihatsu", "Ayla", "Mobil kecil yang irit bahan bakar dan nyaman untuk kota.", 2023, 220000, 5, "Manual", "Petrol", "images/ayla/TRAC_City_Car_Daihatsu_Ayla_Var_01_9327aa9f6c.webp")
    add_car("BMW", "5 Series", "Sedan mewah dengan teknologi tinggi dan kenyamanan maksimal.", 2021, 1500000, 5, "Automatic", "Petrol", "images/bmw_5_series/TRAC_Lux_Car_BMW_5_Series_76b02f8897.webp")
    add_car("BMW", "320i", "Sedan sporty dengan performa tinggi dan desain elegan.", 2020, 1300000, 5, "Automatic", "Petrol", "images/BMW_3201/TRAC_Lux_Car_BMW_320i_17e628ee3e.webp")
    add_car("BMW", "X3", "SUV premium dengan kenyamanan dan fitur canggih.", 2022, 1800000, 5, "Automatic", "Petrol", "images/BMW_X_3/TRAC_Lux_Car_BMW_X_3_9cacbe2810.webp")
    
    add_car("Toyota", "Calya", "Mobil keluarga dengan ruang luas dan fitur keselamatan.", 2023, 300000, 7, "Manual", "Petrol", "images/Calya/TRAC_City_Car_Toyota_Calya_Varian_01_7a5050dc23.webp")
    add_car("Toyota", "Yaris", "Hatchback stylish dengan performa tangguh dan fitur modern.", 2022, 350000, 5, "Automatic", "Petrol", "images/Yaris/TRAC_City_Car_Toyota_Yaris_d7a410503d.webp")

    today = datetime.date.today()
    rent_car(2, 1, today, today + datetime.timedelta(days=3))  # User 2 menyewa mobil ID 1
    rent_car(2, 2, today, today + datetime.timedelta(days=3))  # User 2 menyewa mobil ID 1
    rent_car(3, 2, today, today + datetime.timedelta(days=3))  # User 2 menyewa mobil ID 1
    rent_car(4, 2, today, today + datetime.timedelta(days=3))  # User 2 menyewa mobil ID 1
    rent_car(5, 2, today + datetime.timedelta(days=4), today + datetime.timedelta(days=7))  # User 2 menyewa mobil ID 1



    rent_car(2, 3, today, today + datetime.timedelta(days=3))  # User 2 menyewa mobil ID 1

    rent_car(2, 4, today, today + datetime.timedelta(days=3))  # User 2 menyewa mobil ID 1

    rent_car(2, 5, today, today + datetime.timedelta(days=3))  # User 2 menyewa mobil ID 1

    
    customer_history(2)  # Cek history customer
    admin_history()  # Cek history admin
    admin_approve(2, 1)  # Admin menyetujui rental
    admin_approve(2, 2)  # Admin menyetujui rental
    complete_rental(1)  # Tandai rental sebagai selesai
    admin_history()  # Cek kembali setelah selesai

