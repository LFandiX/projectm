from flask import Flask, render_template, request, redirect, url_for, jsonify, session, send_file, Response
from functools import wraps
import pandas as pd
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from dotenv import load_dotenv
import os
import subprocess

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set secret key
app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")

# Safety check
if not app.config['SECRET_KEY']:
    raise RuntimeError("FLASK_SECRET_KEY belum diset di .env")


# --- KONFIGURASI DATABASE ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'FNDDatabase.1',
    'database': 'toko_digital'
}
import os

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', 'FNDDatabase.1')
DB_NAME = os.getenv('DB_NAME', 'toko_digital')
# --- KONFIGURASI BACKUP ---
BACKUP_DIR = "backups"

if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

def get_db():
    return mysql.connector.connect(**db_config)

# --- CUSTOM DECORATOR UNTUK PROTEKSI LOGIN ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'loggedin' not in session or session.get('role') != 'admin':
            return "Akses Ditolak: Anda bukan Admin!", 403
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTE AUTHENTICATION ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']
        
        try:
            db = get_db()
            cursor = db.cursor(dictionary=True)
            # Cari user berdasarkan username saja
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            db.close()
            
            # Cek apakah user ada DAN password hash-nya cocok
            if user and check_password_hash(user['password'], password_input):
                session['loggedin'] = True
                session['id'] = user['id']
                session['username'] = user['username']
                session['nama'] = user['nama_lengkap']
                session['role'] = user['role']
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', msg='Username atau Password salah!')
        except Exception as e:
            return f"Database Error: {str(e)}"
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
# --- ROUTE DASHBOARD ---


@app.route('/')
@login_required
def dashboard():
    try:
        from datetime import datetime, timedelta
        db = get_db()
        cursor = db.cursor(dictionary=True)
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

        # 1. Omzet Hari Ini
        cursor.execute("SELECT SUM(total_harga) as total FROM transactions WHERE DATE(created_at) = %s", (today,))
        omzet_today = cursor.fetchone()['total'] or 0

        # 2. Jumlah Transaksi Hari Ini
        cursor.execute("SELECT COUNT(id) as jml FROM transactions WHERE DATE(created_at) = %s", (today,))
        transaksi_today = cursor.fetchone()['jml'] or 0

        # 3. Produk Hampir Habis (Stok < 5)
        cursor.execute("SELECT COUNT(id) as jml FROM products WHERE stok < 5 AND is_active = 1")
        low_stock = cursor.fetchone()['jml'] or 0

        # 4. Data untuk Grafik (7 Hari Terakhir)
        cursor.execute("""
            SELECT DATE(created_at) as tgl, SUM(total_harga) as total 
            FROM transactions 
            GROUP BY DATE(created_at) 
            ORDER BY tgl DESC LIMIT 7
        """)
        chart_data = cursor.fetchall()

        cursor.close()
        db.close()
        
        return render_template('dashboard.html', 
                            omzet=omzet_today, 
                            transaksi=transaksi_today, 
                            low_stock=low_stock,
                            chart_data=chart_data)
    except Exception as e:
        return f"Error: {str(e)}"

# --- ROUTES INVENTORI ---

# --- 1. Update List Inventori ---
@app.route('/inventory')
@login_required
def inventory_list():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        # TAMBAHKAN: WHERE is_active = 1
        cursor.execute("SELECT * FROM products WHERE is_active = 1 ORDER BY id DESC")
        items = cursor.fetchall()
        cursor.close()
        db.close()
        return render_template('inventori.html', items=items)
    except Exception as e:
        return f"Error: {e}"




# --- 3. Update Fungsi Delete (Ubah ke Soft Delete) ---
@app.route('/inventory/delete/<int:id>')
@login_required
def delete_product(id):
    try:
        db = get_db()
        cursor = db.cursor()
        # UBAH: Dari DELETE menjadi UPDATE is_active = 0
        cursor.execute("UPDATE products SET is_active = 0 WHERE id = %s", (id,))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('inventory_list'))
    except Exception as e:
        return f"Gagal menghapus: {e}"


@app.route('/inventory/add', methods=['POST'])
@login_required
def add_product():
    try:
        # Mengambil data dari form
        sku = request.form['sku']
        nama = request.form['nama']
        harga_beli = request.form['harga_beli']
        harga_jual = request.form['harga_jual']
        stok = request.form['stok']
        
        db = get_db()
        cursor = db.cursor()
        # Query INSERT lengkap
        sql = """INSERT INTO products (sku, nama_barang, harga_beli, harga_jual, stok) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (sku, nama, harga_beli, harga_jual, stok))
        db.commit()
        cursor.close()
        db.close()
        
        return redirect(url_for('inventory_list'))
    except Exception as e:
        # Menampilkan pesan jika SKU duplikat atau ada error DB lainnya
        return f"Gagal menambahkan produk: {str(e)}", 500

@app.route('/inventory/get/<int:id>')
@login_required
def get_product(id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
        product = cursor.fetchone()
        cursor.close()
        db.close()
        return jsonify(product) if product else (jsonify({"error": "Not Found"}), 404)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/inventory/update', methods=['POST'])
@login_required
def update_product():
    data = (
        request.form['nama'],
        request.form['harga_beli'],
        request.form['harga_jual'],
        request.form['stok'],
        request.form['id']
    )
    db = get_db()
    cursor = db.cursor()
    sql = """UPDATE products SET nama_barang=%s, harga_beli=%s, harga_jual=%s, stok=%s WHERE id=%s"""
    cursor.execute(sql, data)
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('inventory_list'))

@app.route('/inventory/stock-entry', methods=['POST'])
@login_required
def stock_entry():
    product_id = request.form['id']
    jumlah_masuk = int(request.form['jumlah_masuk'])
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE products SET stok = stok + %s WHERE id = %s", (jumlah_masuk, product_id))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('inventory_list'))


@app.route('/inventory/adjust', methods=['POST'])
@login_required
def stock_adjustment():
    product_id = request.form.get('product_id')
    stok_fisik = int(request.form.get('stok_fisik'))
    keterangan = request.form.get('keterangan')
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    try:
        # Ambil stok lama untuk menghitung selisih
        cursor.execute("SELECT stok FROM products WHERE id = %s", (product_id,))
        old_stok = cursor.fetchone()['stok']
        selisih = stok_fisik - old_stok
        
        # 1. Update tabel products
        cursor.execute("UPDATE products SET stok = %s WHERE id = %s", (stok_fisik, product_id))
        
        # 2. Simpan ke riwayat stock_adjustments
        cursor.execute("""INSERT INTO stock_adjustments 
                         (product_id, qty_sebelum, qty_sesudah, selisih, keterangan, user_id) 
                         VALUES (%s, %s, %s, %s, %s, %s)""",
                       (product_id, old_stok, stok_fisik, selisih, keterangan, session['id']))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error Adjust: {e}")
    finally:
        cursor.close()
        db.close()
        
    return redirect(url_for('inventory_list'))

@app.route('/inventory/adjustment-history')
@login_required
def adjustment_history():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Query untuk mengambil data riwayat beserta nama produk dan nama user yang mengedit
    query = """
        SELECT 
            sa.*, 
            p.nama_barang, 
            p.sku,
            u.username as nama_user 
        FROM stock_adjustments sa
        JOIN products p ON sa.product_id = p.id
        JOIN users u ON sa.user_id = u.id
        ORDER BY sa.created_at DESC
    """
    cursor.execute(query)
    histories = cursor.fetchall()
    
    cursor.close()
    db.close()
    return render_template('adjustment_history.html', histories=histories)

# --- ROUTE USER MANAGEMENT ---

@app.route('/users')
@login_required
@admin_only
def user_management():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, username, role, nama_lengkap FROM users")
    all_users = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('users.html', users=all_users)

@app.route('/users/add', methods=['POST'])
@login_required
@admin_only
def add_user():
    try:
        username = request.form['username']
        password_plain = request.form['password']
        role = request.form['role']
        nama = request.form['nama_lengkap']
        
        hashed_password = generate_password_hash(password_plain)
        
        db = get_db()
        cursor = db.cursor()
        sql = "INSERT INTO users (username, password, role, nama_lengkap) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, hashed_password, role, nama))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('user_management'))
    except Exception as e:
        print(f"DEBUG ERROR: {e}") # Ini akan memunculkan error asli di terminal VS Code
        return f"Terjadi Kesalahan: {e}", 500

@app.route('/users/delete/<int:id>')
@login_required
@admin_only
def delete_user(id):
    # Mencegah admin menghapus dirinya sendiri
    if id == session.get('id'):
        return "Anda tidak bisa menghapus akun sendiri!", 400
        
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('user_management'))

# UPDATE pada route /login (Pastikan session menyimpan role)
# Di dalam if user:


import json

@app.route('/kasir')
@login_required
def kasir_page():
    return render_template('kasir.html')

@app.route('/inventory/get_by_sku/<sku>')
@login_required
def get_by_sku(sku):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM products WHERE sku = %s", (sku,))
    product = cursor.fetchone()
    cursor.close()
    db.close()
    return jsonify(product) if product else jsonify({"error": "Not Found"})

@app.route('/kasir/checkout', methods=['POST'])
@login_required
def checkout():
    # Ambil data dari form
    raw_cart_data = request.form.get('cart_data')
    bayar = float(request.form.get('bayar', 0))
    
    # Konversi string JSON ke List Python
    # cart_data = json.loads(raw_cart_data)
    cart_data = json.loads(request.form.get('cart_data'))
    
    # PERBAIKAN DI SINI: Pastikan harga dan qty dikonversi ke angka
    try:
        total_harga = sum(float(item['harga']) * int(item['qty']) for item in cart_data)
    except (ValueError, TypeError) as e:
        return f"Error data keranjang: {str(e)}", 400

    kembali = bayar - total_harga
    invoice = "INV-" + datetime.now().strftime("%Y%m%d%H%M%S")

    db = get_db()
    cursor = db.cursor()
    
    try:
        # 1. Simpan Header Transaksi
        cursor.execute("""INSERT INTO transactions (no_invoice, total_harga, bayar, kembali, user_id) 
                          VALUES (%s, %s, %s, %s, %s)""", 
                       (invoice, total_harga, bayar, kembali, session['id']))
        transaction_id = cursor.lastrowid
        
        # 2. Simpan Detail & Kurangi Stok
        for item in cart_data:
            item_harga = float(item['harga'])
            item_qty = int(item['qty'])
            subtotal = item_harga * item_qty
            cursor.execute("""INSERT INTO transaction_details (transaction_id, product_id, qty, harga_jual, subtotal) 
                              VALUES (%s, %s, %s, %s, %s)""",
                           (transaction_id, item['id'], item['qty'], item['harga'], subtotal))
            
            # PENTING: Update Stok di tabel products
            cursor.execute("UPDATE products SET stok = stok - %s WHERE id = %s", (item['qty'], item['id']))
            
        db.commit()

        
        # Ambil data transaksi yang baru saja dimasukkan untuk ditampilkan di nota
        return jsonify({
            "status": "success",
            "invoice": invoice,
            "total": total_harga,
            "bayar": bayar,
            "kembali": kembali,
            "items": cart_data,
            "kasir": session['nama'],
            "waktu": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    except Exception as e:
        if db: db.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if db: db.close()



@app.route('/inventory/get_all_json')
@login_required
def get_all_json():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        # TAMBAHKAN: AND is_active = 1
        cursor.execute("SELECT id, sku, nama_barang, harga_jual, stok FROM products WHERE is_active = 1 AND stok > 0")
        products = cursor.fetchall()
        cursor.close()
        db.close()
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/transactions')
@login_required
def transaction_history():
    # Ambil parameter filter dari URL
    filter_date = request.args.get('date') # Format: YYYY-MM-DD
    filter_month = request.args.get('month') # Format: MM
    filter_year = request.args.get('year') # Format: YYYY

    db = get_db()
    cursor = db.cursor(dictionary=True)
    
    # Query Dasar
    query = """
        SELECT t.*, u.nama_lengkap as nama_kasir 
        FROM transactions t 
        JOIN users u ON t.user_id = u.id 
        WHERE 1=1
    """
    params = []

    # Tambahkan Logika Filter
    if filter_date:
        query += " AND DATE(t.created_at) = %s"
        params.append(filter_date)
    if filter_month:
        query += " AND MONTH(t.created_at) = %s"
        params.append(filter_month)
    if filter_year:
        query += " AND YEAR(t.created_at) = %s"
        params.append(filter_year)

    query += " ORDER BY t.created_at DESC"
    
    cursor.execute(query, params)
    history = cursor.fetchall()
    cursor.close()
    db.close()
    
    return render_template('riwayat.html', history=history)

# API Detail Transaksi (Tetap sama seperti sebelumnya namun pastikan mengembalikan data lengkap)
@app.route('/transactions/detail/<int:id>')
@login_required
def transaction_detail(id):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    # Ambil data header dan detail sekaligus
    cursor.execute("""
        SELECT td.*, p.nama_barang, t.no_invoice, t.total_harga, t.bayar, t.kembali, t.created_at, u.nama_lengkap as nama_kasir
        FROM transaction_details td
        JOIN products p ON td.product_id = p.id
        JOIN transactions t ON td.transaction_id = t.id
        JOIN users u ON t.user_id = u.id
        WHERE td.transaction_id = %s
    """, (id,))
    details = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(details)


@app.route('/settings/database')
# @login_required # Pastikan decorator ini sudah kamu definisikan
def database_settings():
    # Mengambil daftar file backup dan mengurutkan dari yang terbaru
    files = sorted(os.listdir(BACKUP_DIR), reverse=True)
    return render_template('database_settings.html', files=files)

# --- ROUTE PROSES BACKUP ---
@app.route('/settings/backup')
def backup_db():
    filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    filepath = os.path.join(BACKUP_DIR, filename)
    
    try:
        # Jika menggunakan XAMPP di Windows, biasanya path lengkapnya:
        # C:\\xampp\\mysql\\bin\\mysqldump.exe
        
        with open(filepath, 'w') as f:
            # Perintah subprocess untuk mengeksekusi mysqldump
            # Jika ada password, tambahkan f"-p{DB_PASS}" di dalam list
            
            result = subprocess.run(
                ['mysqldump', '-u', DB_USER, DB_NAME], 
                stdout=f, 
                stderr=subprocess.PIPE,
                text=True,
                shell=True # Gunakan shell=True di Windows agar perintah dikenali
            )
            
        if result.returncode != 0:
            # Jika mysqldump gagal, hapus file kosong yang terlanjur dibuat
            if os.path.exists(filepath):
                os.remove(filepath)
            print(f"Error mysqldump: {result.stderr}")
            return f"Gagal Backup: {result.stderr}", 500
            
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        print(f"Exception: {str(e)}")
        return f"Terjadi kesalahan sistem: {str(e)}", 500
    
    return redirect(url_for('database_settings'))

# --- ROUTE EXPORT EXCEL ---
@app.route('/reports/export', methods=['POST'])
def export_report():
    month = request.form.get('month')
    year = request.form.get('year')
    
    try:
        # Gunakan koneksi database kamu
        from app import get_db # Sesuaikan dengan cara kamu import get_db
        db = get_db()
        
        query = """
            SELECT t.no_invoice, t.created_at as tanggal, t.total_harga, 
                   t.bayar, t.kembali, u.username as kasir
            FROM transactions t
            JOIN users u ON t.user_id = u.id
            WHERE MONTH(t.created_at) = %s AND YEAR(t.created_at) = %s
        """
        
        # Baca data menggunakan pandas
        df = pd.read_sql(query, db, params=(month, year))
        db.close()

        if df.empty:
            return "<script>alert('Data tidak ditemukan untuk periode ini'); window.history.back();</script>"

        # Buat file excel sementara
        output_file = f"Laporan_Penjualan_{month}_{year}.xlsx"
        df.to_excel(output_file, index=False)
        
        return send_file(output_file, as_attachment=True)
        
    except Exception as e:
        return f"Gagal Export: {str(e)}", 500


if __name__ == '__main__':
    # host='0.0.0.0' sangat penting agar Docker bisa diakses
    app.run(debug=True, host='0.0.0.0', port=5000)