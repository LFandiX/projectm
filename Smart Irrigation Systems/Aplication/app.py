'''
Project Smart Irigation System with AI and Wazuh Integration
--Web Application--

Kelompok:
- Alfandi Wijaya (232200156)
- Alvern Brainard (232200346)
- Petra Gamma Setya Agatha (232300115)

'''
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import random
from flask_mqtt import Mqtt
import requests
import joblib
import pandas as pd
import logging
import os
from functools import wraps

# --- Konfigurasi Aplikasi ---
app = Flask(__name__)
app.secret_key = 'kunci_rahasia_sangat_aman'  

# --- KONFIGURASI LOGGING (WAZUH) ---
# log_dir = '/var/log/smart_garden'
log_dir = 'C:\logs'
# Cek apakah folder ada, jika tidak buat folder tersebut
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir, mode=0o755) # Permission rwxr-xr-x
        print(f"[INFO] Folder {log_dir} berhasil dibuat.")
    except OSError as e:
        # Jika permission denied (biasanya karena belum sudo), fallback ke folder lokal aplikasi
        print(f"[WARN] Gagal membuat {log_dir} (Permission Denied). Menggunakan folder 'logs' lokal.")
        log_dir = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

# Path lengkap file log
log_file_path = os.path.join(log_dir, 'serangan.log')

# Konfigurasi Log Handler
logging.basicConfig(
    filename=log_file_path, 
    level=logging.INFO, 
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# --- Konfigurasi Database ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///irrigation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Konfigurasi Waktu Offline ---
ESP_OFFLINE_THRESHOLD = 300 
WEATHER_API_URL = "https://api.weatherapi.com/v1/current.json?key=ef75434afd084933a3a64248251411&q=-6.2,106.816666"

# --- Status Pompa Global ---
LAST_PUMP_STATUS = "OFF"

# --- Model Database ---
class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    soil_moisture = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    rainfall = db.Column(db.Float, nullable=True) 

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            "soil_moisture": self.soil_moisture,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "rainfall": self.rainfall
        }

# --- KONFIGURASI MQTT ---
app.config['MQTT_BROKER_URL'] = '31.97.111.124'  
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'iot-class'  
app.config['MQTT_PASSWORD'] = 'iot'
app.config['MQTT_REFRESH_TIME'] = 1.0
app.config['MQTT_TLS_ENABLED'] = False

mqtt = Mqtt(app)

# --- DECORATOR: LOGIN REQUIRED ---
# Fungsi ini memaksa user login sebelum bisa akses halaman
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Harap login terlebih dahulu.', 'danger')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- FUNGSI BANTUAN ---

def get_rainfall_from_api():
    """Mengambil data precip_mm dari WeatherAPI.com"""
    try:
        response = requests.get(WEATHER_API_URL, timeout=5)
        data = response.json()
        curah_hujan = data.get('current', {}).get('precip_mm', 0.0)
        return curah_hujan
    except Exception as e:
        print(f"Gagal ambil data cuaca: {e}")
        return 0.0 

def get_predict_from_api():
    """Mengambil data cuaca lengkap untuk prediksi"""
    try:
        response = requests.get(WEATHER_API_URL, timeout=5)
        data = response.json()
        
        rainfall = data.get('current', {}).get('precip_mm', 0.0)
        wind_speed = data.get('current', {}).get('wind_kph', 0.0)
        preasure = (data.get('current', {}).get('pressure_mb'))/10
        air_humidity = data.get('current', {}).get('humidity', 0.0)
        wind_gust =  data.get('current', {}).get('gust_kph', 0.0)
        return [rainfall,wind_speed,preasure,air_humidity,wind_gust]
    except Exception as e:
        print(f"Gagal ambil data cuaca: {e}")
        return [0.0,0.0,0.0,0.0,0.0] 

# --- MQTT HANDLERS ---

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\n" + "="*40)
        print("✅ FLASK BERHASIL tersambung KE BROKER!")
        print("="*40 + "\n")
        mqtt.subscribe('kebun/data')
    else:
        print(f"❌ GAGAL tersambung. Kode Error: {rc}")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    global LAST_PUMP_STATUS
    try:
        payload_str = message.payload.decode()
        # print(f"Pesan Masuk [{message.topic}]: {payload_str}")
        
        data = json.loads(payload_str)
        
        suhu = data.get('suhu_udara', 0)
        humi = data.get('kelembapan_udara', 0)
        tanah = data.get('kelembapan_tanah', 0)
        
        if 'pompa_status' in data:
            LAST_PUMP_STATUS = data['pompa_status']

        hujan_api = get_rainfall_from_api()

        with app.app_context():
            new_data = SensorData(
                soil_moisture=tanah,
                humidity=humi,
                temperature=suhu,
                rainfall=hujan_api  
            )
            db.session.add(new_data)
            db.session.commit()
            print(f"--> Data Saved. Tanah: {tanah}%, Hujan: {hujan_api} mm")

    except Exception as e:
        print("Error memproses MQTT:", e)

# --- ROUTES: AUTHENTICATION (LOGIN) ---

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        ip_address = request.remote_addr
        
        # --- HARDCODED CREDENTIALS ---
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['user'] = username
            
            # LOG SUKSES KE FILE
            log_msg = f"CustomApp: LOGIN_SUCCESS User '{username}' from IP {ip_address}"
            logging.info(log_msg)
            print(f"[+] {log_msg}")
            
            return redirect(url_for('home'))
        else:
            # LOG GAGAL KE FILE (TARGET WAZUH)
            log_msg = f"CustomApp: LOGIN_FAILED User '{username}' from IP {ip_address}"
            logging.info(log_msg)
            print(f"[-] {log_msg}")
            
            error = "Password atau Username Salah!"
            
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


@app.route('/')
@login_required  
def home():
    return render_template('home.html')

@app.route('/history')
@login_required
def history():
    return render_template('history.html')

@app.route('/status')
@login_required
def status():
    esp_status = "Unknown"
    last_seen_time = None
    
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
    
    if latest_data:
        last_seen_time = latest_data.timestamp
        time_diff = (datetime.utcnow() - last_seen_time).total_seconds()
        esp_status = "Offline" if time_diff > ESP_OFFLINE_THRESHOLD else "Online"
    
    page = request.args.get('page', 1, type=int)
    pagination = SensorData.query.order_by(SensorData.timestamp.desc()).paginate(page=page, per_page=15, error_out=False)
    
    return render_template('status.html', esp_status=esp_status, last_seen_time=last_seen_time, pagination=pagination)


@app.route('/api/latest-status')
@login_required # Proteksi API agar tidak bisa diakses publik tanpa login
def get_latest_status():
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
    
    if latest_data:
        data_json = latest_data.to_dict()
    else:
        data_json = {"soil_moisture": 0, "humidity": 0, "temperature": 0, "rainfall": 0}
    
    return jsonify({
        "sensor_data": data_json,
        "pump_status": {"state": LAST_PUMP_STATUS} 
    })

@app.route('/api/chart-data')
@login_required
def get_chart_data():
    data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(50).all()
    data.reverse() 
    chart_data = {
        "labels": [d.timestamp.strftime('%H:%M:%S') for d in data],
        "soil_moisture": [d.soil_moisture for d in data],
        "humidity": [d.humidity for d in data],
        "temperature": [d.temperature for d in data],
        "rainfall": [d.rainfall for d in data]
    }
    return jsonify(chart_data)

@app.route('/irrigate', methods=['POST'])
@login_required 
def manual_irrigate():
    msg = "MANUAL" 
    mqtt.publish('kebun/pompa', msg)
    print(f"PERINTAH MANUAL: Mengirim '{msg}' ke topik 'kebun/pompa'")
    
    # Log aktivitas pompa juga (Opsional)
    user = session.get('user', 'unknown')
    logging.info(f"CustomApp: PUMP_TRIGGERED by User '{user}'")

    return jsonify({
        "message": "Menyiram tanaman (2 Detik)...", 
        "state": "ON" 
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        soil_moist = data['kelembapan_tanah']
        air_temp = data['suhu_udara']
        humidity = data["kelembapan_udara"]
        
        apidata = get_predict_from_api()

        data_baru = pd.DataFrame({
            'Soil Moisture': [soil_moist],
            'Air temperature (C)': [air_temp],
            'Wind speed (Km/h)' : [apidata[1]],
            'Air humidity (%)': [humidity],
            'Wind gust (Km/h)': [apidata[4]],
            'Pressure (KPa)': [apidata[2]],
            'rainfall' : [apidata[0]]
        })

        model = joblib.load('model_irigasi_logreg.joblib')
        hasil_prediksi_angka = model.predict(data_baru)

        return jsonify({
            "predict":f"{hasil_prediksi_angka[0]}", 
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':     
    print(f"[*] Aplikasi Smart Garden berjalan.")
    print(f"[*] Log Keamanan aktif di: {log_file_path}")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)



# Komitmen Integritas
# “Di hadapan TUHAN yang hidup, saya menegaskan bahwa saya tidak memberikan 
# maupun menerima bantuan apapun — baik lisan, tulisan, maupun elektronik — 
# di dalam ujian ini selain daripada apa yang telah diizinkan oleh pengajar, 
# dan tidak akan menyebarkan baik soal maupun jawaban ujian kepada pihak lain.