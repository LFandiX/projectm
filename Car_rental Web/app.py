from flask import Flask, session, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import datetime

app = Flask(__name__)

app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "FNDDatabase.1"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_DB"] = "rental_mobil"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.secret_key = "secret"

mysql = MySQL(app)

@app.route('/')
def main():
    return redirect(url_for('home'))

# Authentication Section

@app.route('/login', methods=['POST', 'GET'])
def login():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        user = request.form['username']
        password = request.form['password']
        cur.execute(f'''SELECT * FROM users WHERE username = "{user}"''')
        user_check = cur.fetchall()
        print(user_check)
        if len(user_check) == 0:
            return render_template('login.html', user_exists=False)
        else:   
            if user_check[0]['password'] == password:
                session['user'] = user_check[0]
                if user_check[0]['role'] == 'Admin':
                    return redirect(url_for('admin'))
                return redirect(url_for('home'))
            else:
                return render_template('login.html', password_incorrect=True)
    else:
        if "user" in session and session['user']['role'] == 'Admin':
            return redirect(url_for('admin'))
        elif 'user' in session:
            return redirect(url_for('home'))
        
        return render_template('login.html', user_exists=True, password_incorrect=False)

@app.route('/register', methods=['POST', 'GET'])
def register():
    cur = mysql.connection.cursor()
    if request.method == "POST":
        user = request.form['username']
        password = request.form['password']
        cur.execute(f'''SELECT * FROM users WHERE username = "{user}"''')
        user_check = cur.fetchall()
        if len(user_check) == 0:
            cur.execute(f'''INSERT INTO users (username, password, role) VALUES ("{user}", "{password}", "Customer")''')
            mysql.connection.commit()
            cur.execute(f'''SELECT * FROM users WHERE username = "{user}"''')
            user_info = cur.fetchall()
            session['user'] = user_info[0]
            return redirect(url_for('login'))
        else:
            return render_template('register.html', user_exists=True)
    else:
        if "user" in session and session['user']['role'] == 'Admin':
            return redirect(url_for('admin'))
        elif 'user' in session:
            return redirect(url_for('home'))
        return render_template('register.html', user_exists=False)
    
@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user', None)
        return redirect(url_for('home'))
    return redirect(url_for('home'))

# General Section

@app.route('/home')
def home():
    if "user" in session and session['user']['role'] == 'Admin':
        return redirect(url_for('admin'))


    cur = mysql.connection.cursor()
    current_page = request.args.get('page', 1)
    cars = request.args.get('cars', 'all')
    seats = request.args.get('seats', 'all')
    mode = request.args.get('mode', 'all')
    fuel = request.args.get('fuel', 'all')
    status = request.args.get('status', 'all')

    query = "SELECT * FROM cars WHERE 1=1"
    if cars != 'all':
        query += f" AND brand = '{cars}'"
    if seats != 'all':
        query += f" AND seats = {seats}"
    if mode != 'all':
        query += f" AND mode = '{mode}'"
    if fuel != 'all':
        query += f" AND fuel = '{fuel}'"
    if status != 'all':
        query += f" AND status = '{status}'"
    current_page = int(current_page)
    cur.execute(query)
    cars = cur.fetchall()
    cur.execute(f'''SELECT COUNT(*) FROM cars''')
    total_cars = cur.fetchall()[0]['COUNT(*)']
    max_page = total_cars // 20 + 1
    if "user" in session and session['user']['role'] == 'Customer':
        cur.execute(f'''SELECT c.brand, c.model, DATEDIFF(r.end_date, CURDATE()) as days_remaining, c.image_link, r.status
        FROM rentals r
        JOIN cars c ON r.car_id = c.id WHERE r.user_id = {session['user']['id']} ''')
        history = cur.fetchall()
        print(history)
        return render_template('home.html', cars=cars, history=history, page=current_page, max_page=max_page, session_user=session['user'])
    else:
        return render_template('home.html', cars=cars, history=None, page=current_page, max_page=max_page, session_user=None)

@app.route('/about-us')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact_us():
    return render_template('contact.html')

#Admin Section

@app.route('/admin')
def admin():
    if "user" in session and session['user']['role'] == 'Admin':
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM cars WHERE id IN (SELECT distinct car_id FROM rentals WHERE status = 'Waiting For Approval')''')
        rentals= cur.fetchall()
        return render_template('admin.html', rentals=rentals, session_user=session['user'])
    else:
        return redirect(url_for('home'))
    
@app.route('/admin/add', methods=['POST', 'GET'])
def admin_add():
    if request.method == "POST":
        brand = request.form['brand']
        model = request.form['model']
        seats = request.form['seats']
        mode = request.form['mode']
        fuel = request.form['fuel']
        price_per_day = request.form['price_per_day']
        image_link = request.form['image_link']
        cur = mysql.connection.cursor()
        cur.execute(f'''INSERT INTO cars (brand, model, seats, mode, fuel, price_per_day, image_link) VALUES ("{brand}", "{model}", "{seats}", "{mode}", "{fuel}", "{price_per_day}", "{image_link}")''')
        mysql.connection.commit()
        return redirect(url_for('admin_add'))
    return render_template('admin_add.html')

@app.route('/admin/history', methods=['POST', 'GET'])
def admin_history():   
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT u.username, c.brand, c.model, r.start_date, r.end_date, r.total_price, r.status, r.total_days, DATEDIFF(r.end_date, CURDATE()) as days_remaining,c.image_link
    FROM rentals r
    JOIN cars c ON r.car_id = c.id
    join users u on r.user_id = u.id''')
    data = cur.fetchall()
    print(data)
    return render_template('admin_history.html', rentals=data, session_user=session['user'])
    
@app.route('/admin/<carID>', methods=['POST', 'GET'])
def admin_product(carID):
    if "user" in session and session['user']['role'] == 'Admin':
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM cars WHERE id = {carID}''')
        car = cur.fetchall()[0]
        cur.execute(f"""SELECT u.username, r.start_date, r.end_date, r.total_price, c.id
                    FROM rentals r join cars c on r.car_id = c.id 
                    join users u on r.user_id = u.id 
                    WHERE r.car_id = {carID} and r.status = 'Waiting For Approval'""")
        rentals = cur.fetchall()
        if len(rentals) == 0:
            return redirect(url_for('admin'))
        return render_template('admin_product.html', car=car, rentals=rentals)
    else:
        return redirect(url_for('home'))

@app.route('/admin/<carID>/approve', methods=["POST", "GET"])
def admin_approve(carID):
    if "user" in session and session['user']['role'] == 'Admin':
        cur = mysql.connection.cursor()
        username = request.form['username']
        cur.execute(f"UPDATE rentals r JOIN users u ON u.id = r.user_id SET r.status = 'Ongoing' WHERE u.username = '{username}' AND r.car_id = {carID}")
        cur.execute(f"UPDATE cars SET status = 'Rented' WHERE id = {carID}")
        cur.execute(f"SELECT r.start_date, r.end_date FROM rentals r JOIN users u ON u.id = r.user_id WHERE u.username = '{username}' AND r.car_id = {carID}")
        approved_rental = cur.fetchone()
        start_date = approved_rental['start_date']
        end_date = approved_rental['end_date']
        cur.execute(f"""
            DELETE r FROM rentals r 
            JOIN users u ON u.id = r.user_id 
            WHERE r.car_id = {carID} 
            AND r.status = 'Waiting For Approval' 
            AND (
                (r.start_date BETWEEN '{start_date}' AND '{end_date}') OR 
                (r.end_date BETWEEN '{start_date}' AND '{end_date}') OR 
                (r.start_date <= '{start_date}' AND r.end_date >= '{end_date}')
            )
        """)
        
        mysql.connection.commit()
        return redirect(url_for('admin_product', carID=carID))
    else:
        return redirect(url_for('home'))

@app.route('/admin/<carID>/reject', methods=["POST", "GET"])
def admin_reject(carID):
    if "user" in session and session['user']['role'] == 'Admin':
        cur = mysql.connection.cursor()
        username = request.form['username']
        cur.execute(f"Delete r from rentals r join users u on u.id = r.user_id where u.username = '{username}' AND r.car_id = {carID}")
        mysql.connection.commit()
        return redirect(url_for('admin_product', carID=carID))
    else:
        return redirect(url_for('home'))

# Rental Section

@app.route('/product/<carID>')
def product(carID):
    if "user" in session and session['user']['role'] == 'Admin':
        return redirect(url_for('admin'))
    cur = mysql.connection.cursor()
    cur.execute(f'''SELECT * FROM cars WHERE id = {carID}''')
    car = cur.fetchall()[0]
    print(session)
    if "user" in session and session['user']['role'] == 'Customer':
        cur.execute(f'''SELECT distinct c.id FROM rentals r join cars c on r.car_id = c.id 
                    WHERE r.user_id = {session['user']['id']} AND (r.status = 'Ongoing' OR r.status = 'Waiting For Approval')''')
        history = [x['id'] for x in cur.fetchall()]

        print(session)
        print(history)
        return render_template('products.html', car=car, history=history, session_user=session['user'])
    return render_template('products.html', car=car, history=[], session_user=None)

@app.route('/product/rent/<carID>', methods=['POST', 'GET'])
def rent(carID):
    if "user" in session and session['user']['role'] == 'Customer':
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT * FROM cars WHERE id = {carID}''')
        car = cur.fetchall()[0]
        if request.method == "POST":
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            total_price = car['price_per_day'] * (datetime.datetime.strptime(end_date, '%Y-%m-%d') - datetime.datetime.strptime(start_date, '%Y-%m-%d')).days
            cur.execute(f'''INSERT INTO rentals (user_id, car_id, start_date, end_date, total_price) VALUES ("{session['user']['id']}", "{carID}", "{start_date}", "{end_date}", "{total_price}")''')
            mysql.connection.commit()
            return redirect(url_for('home'))
        return render_template('rent_confirm.html')
    else:
        if "user" in session and session['user']['role'] == 'Admin':
            return redirect(url_for('admin'))
        return redirect(url_for('login'))


@app.route('/management')
def history():
        cur = mysql.connection.cursor()
        status = request.args.get('status', 'all')
        query = '''
        SELECT u.username, c.brand, c.model, r.start_date, r.end_date, r.total_price, r.status, c.image_link
        FROM rentals r
        JOIN cars c ON r.car_id = c.id 
        join users u on r.user_id = u.id WHERE 1=1 '''
        if status != 'all':
            query += f" AND r.status = '{status}'"
        cur.execute(query)
        data = cur.fetchall()
        return render_template('management.html', rentals=data)


if __name__ == '__main__':
    app.run(debug=True)

