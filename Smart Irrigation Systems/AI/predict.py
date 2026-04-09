'''
Project Smart Irigation System with AI and Wazuh Integration
--Model Predict Usage--

Kelompok:
- Alfandi Wijaya (232200156)
- Alvern Brainard (232200346)
- Petra Gamma Setya Agatha (232300115)

'''

import joblib
import pandas as pd

# --- 1. LOAD MODEL & ENCODER ---
model = joblib.load('model_irigasi_logreg.joblib')


# --- 2. SIAPKAN DATA BARU ---
data_baru = pd.DataFrame({
    'Soil Moisture': [50.35],
    'Air temperature (C)': [33.0],
    'Wind speed (Km/h)' : [14.0],
    'Air humidity (%)': [53.0],
    'Wind gust (Km/h)': [16.2],
    'Pressure (KPa)': [100.5],
    'rainfall' : [0.0]
})

# --- 3. PREDIKSI ---
hasil_prediksi_angka = model.predict(data_baru)

print(f"Prediksi Angka: {hasil_prediksi_angka[0]}")


# Komitmen Integritas
# “Di hadapan TUHAN yang hidup, saya menegaskan bahwa saya tidak memberikan 
# maupun menerima bantuan apapun — baik lisan, tulisan, maupun elektronik — 
# di dalam ujian ini selain daripada apa yang telah diizinkan oleh pengajar, 
# dan tidak akan menyebarkan baik soal maupun jawaban ujian kepada pihak lain.