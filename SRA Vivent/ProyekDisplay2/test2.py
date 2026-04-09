import cv2
import numpy as np

# --- Konstanta Visual ---
# Ukuran layar simulasi
W, H = 1024, 600

# Definisi Warna (BGR Format)
COLOR_BACKGROUND = (0, 0, 0)         # Hitam
COLOR_MAIN_PANEL_BG = (50, 50, 50)   # Abu-abu gelap untuk panel utama
COLOR_GRAY_BG = (30, 30, 30)         # Abu-abu yang lebih gelap
COLOR_BORDER = (100, 100, 100)       # Abu-abu terang untuk batas
COLOR_WHITE = (255, 255, 255)        # Putih
COLOR_BLUE = (255, 120, 0)           # Biru (untuk nilai tertentu)
COLOR_CYAN = (255, 255, 0)           # Cyan (untuk nilai tertentu)
COLOR_YELLOW = (0, 255, 255)         # Kuning
COLOR_ORANGE = (0, 165, 255)         # Oranye

# Definisi Font
FONT_SMALL_Bottom = cv2.FONT_HERSHEY_SIMPLEX
FONT_LARGE = cv2.FONT_HERSHEY_SIMPLEX

# --- Data Parameter Ventilator ---
# (Label, Nilai, Satuan)
parameter_data = [
    ("Ppeak", "23", "cmH2O", COLOR_YELLOW, FONT_LARGE, 2),  # Kiri Atas
    ("Pmean", "9.2", "cmH2O", COLOR_WHITE, FONT_LARGE, 1), # Kanan Atas
    ("PEEP", "4.9", "cmH2O", COLOR_WHITE, FONT_LARGE, 1),  # Kanan Atas
    ("MVe", "6.23", "L/min", COLOR_CYAN, FONT_LARGE, 2),   # Kiri Tengah
    ("TVe", "518", "mL", COLOR_CYAN, FONT_LARGE, 1),       # Kanan Tengah
    ("ftotal", "12", "/min", COLOR_WHITE, FONT_LARGE, 1),  # Kanan Tengah
    ("FiO2", "21", "vol %", COLOR_WHITE, FONT_LARGE, 2),   # Kiri Bawah
    ("fspn", "0", "/min", COLOR_WHITE, FONT_LARGE, 1),     # Kanan Bawah
    ("TVe/IBW", "7.4", "mL/kg", COLOR_WHITE, FONT_LARGE, 1) # Kanan Bawah
    # Catatan: Data di atas disesuaikan dengan tata letak visual monitor (3 area besar di kiri, 6 area kecil di kanan)
    # serta parameter dari daftar Anda. Beberapa parameter dari daftar Anda ('Insp', 'Pmean') 
    # telah dipindahkan atau diubah posisinya agar sesuai dengan tata letak visual di gambar.
]

# --- Fungsi untuk Menggambar Grafik Ventilator (Dummy) ---
def draw_waveforms(img, x_start, y_start, width, height):
    """Menggambar 3 waveform dasar (Pressure, Flow, Volume) sebagai placeholder."""
    
    # Label Waveforms
    cv2.putText(img, "Paw cmH2O", (x_start + 10, y_start - 5), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)
    cv2.putText(img, "Flow L/min", (x_start + 10, y_start + height//3 - 5), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)
    cv2.putText(img, "Volume mL", (x_start + 10, y_start + 2*height//3 - 5), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)

    # Area tiap grafik
    h = height // 3
    
    # 1. Grafik Tekanan (Paw) - Mirip 'Paruh Burung'
    points_p = np.array([[x_start + 50 + 100*i, y_start + h//2] if i%5==0 else 
                         [x_start + 50 + 100*i, y_start + h//2 - 50] if i%5==1 else 
                         [x_start + 50 + 100*i, y_start + h//2 - 10] if i%5==2 else 
                         [x_start + 50 + 100*i, y_start + h//2 + 20] if i%5==3 else
                         [x_start + 50 + 100*i, y_start + h//2] 
                         for i in range(7)], np.int32)
    cv2.polylines(img, [points_p.reshape((-1, 1, 2))], False, COLOR_ORANGE, 2)
    
    # 2. Grafik Aliran (Flow) - Mirip Kotak/Persegi
    y_flow_base = y_start + h + h//2
    flow_waveform = np.array([
        (x_start + 50, y_flow_base), (x_start + 150, y_flow_base), (x_start + 150, y_flow_base - 30), (x_start + 250, y_flow_base - 30), 
        (x_start + 250, y_flow_base), (x_start + 300, y_flow_base), (x_start + 400, y_flow_base + 40), (x_start + 500, y_flow_base),
        (x_start + 550, y_flow_base), (x_start + 650, y_flow_base), (x_start + 650, y_flow_base - 30), (x_start + 750, y_flow_base - 30),
        (x_start + 750, y_flow_base), (x_start + 800, y_flow_base)
    ], np.int32)
    cv2.polylines(img, [flow_waveform.reshape((-1, 1, 2))], False, COLOR_BLUE, 2)

    # 3. Grafik Volume
    y_vol_base = y_start + 2*h + h//2
    vol_waveform = np.array([
        (x_start + 50, y_vol_base), (x_start + 200, y_vol_base - 40), (x_start + 350, y_vol_base), 
        (x_start + 400, y_vol_base), (x_start + 550, y_vol_base - 40), (x_start + 700, y_vol_base),
        (x_start + 750, y_vol_base)
    ], np.int32)
    cv2.polylines(img, [vol_waveform.reshape((-1, 1, 2))], False, COLOR_BLUE, 2)
    
    # Garis tengah/base (misalnya untuk Flow/Volume nol)
    cv2.line(img, (x_start, y_start + h), (x_start + width, y_start + h), COLOR_BORDER, 1)
    cv2.line(img, (x_start, y_start + 2*h), (x_start + width, y_start + 2*h), COLOR_BORDER, 1)
    
    return img


# --- Fungsi Panel Utama (Grafik & Parameter) ---
def mid_panel(img, parameter_data):
    # Batas area panel kanan
    panel_x_end = W - 184 # Mengasumsikan ada panel samping kanan
    panel_y_start = 100
    panel_height = 485
    
    # 1. Background Panel Utama
    cv2.rectangle(img, (0, panel_y_start), (panel_x_end, panel_y_start + panel_height), COLOR_MAIN_PANEL_BG, -1)
    panel_y_start += 35
    panel_height = 450
    # Background abu-abu untuk area gambar (grafik dan parameter)
    cv2.rectangle(img, (0, panel_y_start), (panel_x_end, panel_y_start + panel_height), COLOR_GRAY_BG, -1)

    # --- Area Grafik (Kiri) ---
    graph_x_start = 10
    graph_width = 725
    graph_y_start = panel_y_start + 10
    graph_height = 430
    
    cv2.rectangle(img, (graph_x_start, graph_y_start), (graph_x_start + graph_width, graph_y_start + graph_height), COLOR_BACKGROUND, -1)
    # Gambar Waveforms Dummy
    img = draw_waveforms(img, graph_x_start, graph_y_start, graph_width, graph_height)
    
    # --- Area Parameter (Kanan) ---
    param_x_start = graph_x_start + graph_width + 10
    param_width = 340
    param_y_start = graph_y_start
    param_height = graph_height
    
    cv2.rectangle(img, (param_x_start, param_y_start), (param_x_start + param_width, param_y_start + param_height), COLOR_BACKGROUND, -1)
    
    # Garis Pembatas Vertikal (Kolom Kiri Parameter vs Kolom Kanan Parameter)
    cv2.line(img, (param_x_start + param_width//2, param_y_start), (param_x_start + param_width//2, param_y_start + param_height), COLOR_BORDER, 1)

    # --- Kolom Kiri Parameter (3 Item Besar) ---
    # Ppeak, MVe, FiO2
    param_left_indices = [0, 3, 6]
    for i in range(len(param_left_indices)):
        idx = param_left_indices[i]
        label, value, unit, color, font, scale = parameter_data[idx]

        # Garis pembatas horizontal (hanya untuk i > 0)
        if i > 0:
            cv2.line(img, (param_x_start, param_y_start + i*param_height//3), (param_x_start + param_width//2, param_y_start + i*param_height//3), COLOR_BORDER, 1)

        # Teks Label (misalnya 'Ppeak')
        label_x = param_x_start + 10
        label_y = param_y_start + i*param_height//3 + 20
        cv2.putText(img, label, (label_x, label_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)

        # Teks Satuan (misalnya 'cmH2O')
        unit_x = param_x_start + 10
        unit_y = param_y_start + i*param_height//3 + 40
        cv2.putText(img, unit, (unit_x, unit_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)

        # Teks Nilai (misalnya '23' - Besar dan dijustifikasi kanan)
        value_width = cv2.getTextSize(value, font, scale, 2)[0][0]
        value_x = param_x_start + param_width//2 - value_width - 25 # Justifikasi Kanan
        value_y = param_y_start + i*param_height//3 + 115
        
        cv2.putText(img, value, (value_x, value_y), font, scale, color, 2, cv2.LINE_AA)

    # --- Kolom Kanan Parameter (6 Item Kecil) ---
    # Pmean, PEEP, TVe, ftotal, fspn, TVe/IBW
    param_right_indices = [1, 2, 4, 5, 7, 8]
    for i in range(len(param_right_indices)):
        idx = param_right_indices[i]
        label, value, unit, color, font, scale = parameter_data[idx]

        # Garis pembatas horizontal (hanya untuk i > 0)
        if i > 0:
            cv2.line(img, (param_x_start + param_width//2, param_y_start + i*param_height//6), (param_x_start + param_width, param_y_start + i*param_height//6), COLOR_BORDER, 1)

        # Teks Label (misalnya 'Pmean')
        label_x = param_x_start + param_width//2 + 10
        label_y = param_y_start + i*param_height//6 + 20
        cv2.putText(img, label, (label_x, label_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)
        
        # Teks Satuan (misalnya 'cmH2O')
        unit_x = param_x_start + param_width//2 + 10
        unit_y = param_y_start + i*param_height//6 + 40
        cv2.putText(img, unit, (unit_x, unit_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)

        # Teks Nilai (misalnya '9.2' - Sedang dan dijustifikasi kanan)
        value_width = cv2.getTextSize(value, font, scale, 2)[0][0]
        value_x = param_x_start + param_width - value_width - 25 # Justifikasi Kanan
        value_y = param_y_start + i*param_height//6 + 50
        
        cv2.putText(img, value, (value_x, value_y), font, scale, color, 2, cv2.LINE_AA)

    return img

# --- Main Program ---
# 1. Buat kanvas kosong
canvas = np.zeros((H, W, 3), dtype=np.uint8) 

# 2. Panggil fungsi untuk menggambar panel utama
canvas = mid_panel(canvas, parameter_data)

# 3. Tampilkan hasil (Jika dijalankan di lingkungan yang mendukung GUI/OpenCV)
# cv2.imshow('Ventilator Monitor Simulation', canvas)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Untuk output yang dapat dilihat di sini (tidak dapat menampilkan window cv2), 
# Saya akan menyimpan gambar dan menampilkannya jika memungkinkan.

print("Kode Python OpenCV untuk simulasi monitor ventilator telah dibuat.")
print("Silakan jalankan kode ini di lingkungan Python dengan pustaka 'opencv-python' terinstal untuk melihat output visual.")
print(f"\nParameter yang digunakan:\n{parameter_data}")