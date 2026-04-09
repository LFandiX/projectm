import cv2
import numpy as np
import math
import random
# --- Konfigurasi dan Palet Warna ---
W, H = 1280, 720 # Ukuran window

# Warna yang digunakan (format BGR)
COLOR_BACKGROUND = (25, 25, 35)      # Biru keabu-abuan gelap
COLOR_MAIN_PANEL_BG = (40, 40, 50)   # Latar belakang panel utama di kanan
COLOR_BUTTON_BG = (45, 45, 55)       # Latar belakang tombol default
COLOR_BORDER = (80, 80, 80)          # Warna garis batas
COLOR_WHITE = (255, 255, 255)        # Putih untuk teks
COLOR_STANDBY = (25, 170, 255)       # Oranye/kuning untuk tombol Standby
COLOR_ALARM_RED = (0, 0, 200)        # Merah gelap untuk background alarm
COLOR_GRAY_BG = (60, 60, 70)         # Abu-abu gelap untuk background sekunder
COLOR_LIGHT_GRAY_BG = (90, 90, 100)  # Abu-abu lebih terang untuk elemen sekunder
COLOR_BLACK = (0, 0, 0)              # Hitam
COLOR_BLUE = (255, 120, 0)      # Biru untuk Flow/Volume
COLOR_ORANGE = (0, 165, 255)
# Font yang digunakan
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SMALL = cv2.FONT_HERSHEY_COMPLEX_SMALL

# Definisi Font
FONT_SMALL_Bottom = cv2.FONT_HERSHEY_SIMPLEX
FONT_LARGE = cv2.FONT_HERSHEY_DUPLEX

# --- Fungsi Bantuan untuk Menggambar ---

def put_text_with_icon(img, text, icon_func, x_start, y_center, button_height, color=COLOR_WHITE):
    """Fungsi untuk menempatkan ikon dan teks di tombol."""
    # Gambar ikon
    icon_x = x_start + 18 
    icon_func(img, icon_x, y_center)

    # Posisi teks
    center_x = x_start + 10  # Jarak 20px dari kiri tombol ke ikon
    text_x = center_x + 25 # Jarak 25px dari ikon ke teks
    text_size = cv2.getTextSize(text, FONT_SMALL, 0.6, 1)[0]
    text_y = y_center + text_size[1] // 2
    cv2.putText(img, text, (text_x, text_y), FONT_SMALL, 0.6, color, 1, cv2.LINE_AA)

def put_text(img, text, icon_func, x_start, y_center, button_height, color=COLOR_WHITE):
    """Fungsi untuk menempatkan ikon dan teks di tombol."""
    center_x = x_start + 20  # Jarak 20px dari kiri tombol ke ikon
    text_x = center_x  # Jarak 25px dari ikon ke teks
    text_size = cv2.getTextSize(text, FONT_SMALL, 0.6, 1)[0]
    text_y = y_center + text_size[1] // 2
    cv2.putText(img, text, (text_x, text_y), FONT_SMALL, 0.6, color, 1, cv2.LINE_AA)

# --- Ikon-ikon Khusus ---
def icon_alarm(img, x, y):
    cv2.drawMarker(img, (x,y-5), COLOR_WHITE, markerType=cv2.MARKER_TRIANGLE_UP, markerSize=12, thickness=1)
    cv2.drawMarker(img, (x,y+5), COLOR_WHITE, markerType=cv2.MARKER_TRIANGLE_DOWN, markerSize=12, thickness=1)

def icon_suction(img, x, y):
    # Lingkaran dengan garis diagonal (semacam pipa)
    cv2.circle(img, (x, y), 6, COLOR_WHITE, 1)
    cv2.line(img, (x - 4, y - 4), (x + 4, y + 4), COLOR_WHITE, 1) # Diagonal
    cv2.line(img, (x + 6, y), (x + 12, y), COLOR_WHITE, 1) # "Pipa" keluar

def icon_nebulizer(img, x, y):
    # Awan/kabut
    cv2.circle(img, (x - 4, y + 2), 4, COLOR_WHITE, -1)
    cv2.circle(img, (x + 4, y + 2), 4, COLOR_WHITE, -1)
    cv2.circle(img, (x, y - 2), 4, COLOR_WHITE, -1)
    cv2.line(img, (x - 8, y + 6), (x + 8, y + 6), COLOR_WHITE, 1)

def icon_tools(img, x, y):
    # Gear/roda gigi sederhana
    cv2.circle(img, (x,y), 6, COLOR_WHITE, 1)
    cv2.line(img, (x-7,y), (x-3,y), COLOR_WHITE, 1)
    cv2.line(img, (x+3,y), (x+7,y), COLOR_WHITE, 1)
    cv2.line(img, (x,y-7), (x,y-3), COLOR_WHITE, 1)
    cv2.line(img, (x,y+3), (x,y+7), COLOR_WHITE, 1)

def icon_lock(img, x, y):
    cv2.rectangle(img, (x - 4, y - 2), (x + 4, y + 6), COLOR_WHITE, 1)
    cv2.line(img, (x - 4, y - 2), (x - 4, y - 6), COLOR_WHITE, 1)
    cv2.line(img, (x + 4, y - 2), (x + 4, y - 6), COLOR_WHITE, 1)
    cv2.ellipse(img, (x, y - 6), (4, 4), 0, 0, 180, COLOR_WHITE, 1)

def icon_menu(img, x, y):
    # Tiga garis horizontal
    cv2.line(img, (x - 5, y - 4), (x + 5, y - 4), COLOR_WHITE, 1)
    cv2.line(img, (x - 5, y), (x + 5, y), COLOR_WHITE, 1)
    cv2.line(img, (x - 5, y + 4), (x + 5, y + 4), COLOR_WHITE, 1)

def icon_standby(img, x, y):
    # Ikon power/standby
    cv2.circle(img, (x, y), 8, COLOR_WHITE, 1)
    cv2.line(img, (x, y - 10), (x, y - 3), COLOR_WHITE, 2)


# --- Fungsi Utama untuk Menggambar Panel Kanan ---
def draw_right_panel_revised(img):
    panel_x_start = W - 180  # Posisi X awal untuk panel (lebih ke kiri sedikit)
    panel_y_start = 0       # Dimulai setelah top bar
    panel_width = 170        # Lebar panel
    
    # --- Background Panel Utama ---
    # Gambar background gelap untuk seluruh area tombol
    cv2.rectangle(img, (panel_x_start, panel_y_start), (W, H), COLOR_MAIN_PANEL_BG, -1)
    # Garis pembatas vertikal
    cv2.line(img, (panel_x_start, panel_y_start), (panel_x_start, H), COLOR_BORDER, 1)

    # --- Ukuran Tombol ---
    button_main_width = 140 # Lebar tombol utama
    button_sub_width = 120  # Lebar tombol sub-menu (indentasi)
    button_height = 40      # Tinggi tombol
    margin_y = 20           # Jarak vertikal antar tombol

    current_y_offset = panel_y_start + 10 # Mulai dari bawah top bar, beri sedikit padding

    # --- Tombol Alarms ---
    rect_start = (panel_x_start + (panel_width - button_main_width) // 2, current_y_offset)
    rect_end = (rect_start[0] + button_main_width, current_y_offset + button_height)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BUTTON_BG, -1) # Latar belakang merah
    cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
    put_text_with_icon(img, "Alarms", icon_alarm, rect_start[0], (rect_start[1] + rect_end[1]) // 2, button_height)
    current_y_offset += button_height + margin_y

    # --- Tombol O2 Suction ---
    rect_start = (panel_x_start + (panel_width - button_main_width) // 2, current_y_offset)
    rect_end = (rect_start[0] + button_main_width, current_y_offset + button_height)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BUTTON_BG, -1)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
    put_text_with_icon(img, "O2 Suction", icon_suction, rect_start[0], (rect_start[1] + rect_end[1]) // 2, button_height)
    current_y_offset += button_height + margin_y

    # --- Tombol Nebulizer ---
    rect_start = (panel_x_start + (panel_width - button_main_width) // 2, current_y_offset)
    rect_end = (rect_start[0] + button_main_width, current_y_offset + button_height)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BUTTON_BG, -1)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
    put_text_with_icon(img, "Nebulizer", icon_nebulizer, rect_start[0], (rect_start[1] + rect_end[1]) // 2, button_height)
    current_y_offset += button_height + margin_y

    # --- Tombol Tools (Utama) ---
    rect_start = (panel_x_start + (panel_width - button_main_width) // 2, current_y_offset)
    rect_end = (rect_start[0] + button_main_width, current_y_offset + button_height)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BUTTON_BG, -1)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
    put_text_with_icon(img, "Tools", icon_tools, rect_start[0], (rect_start[1] + rect_end[1]) // 2, button_height)
    current_y_offset += button_height + margin_y

    # --- Sub-menu Tools (P-V Tools, Insp. Hold, PEEPI, Weaning) ---
    # Ini akan di-indentasi (bergeser ke kanan)
    indent_offset = (panel_width - button_sub_width) //2 # Geser lebih ke kanan dari tengah
    
    sub_tools = ["P-V Tools", "Insp. Hold", "PEEPI", "Warning"]
    for label in sub_tools:
        rect_start = (panel_x_start + indent_offset, current_y_offset)
        rect_end = (rect_start[0] + button_sub_width, current_y_offset + button_height)
        cv2.rectangle(img, rect_start, rect_end, COLOR_BUTTON_BG, -1)
        cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
        put_text(img, label, lambda i, x, y: None, rect_start[0], (rect_start[1] + rect_end[1]) // 2, button_height) # No icon for sub-menu
        current_y_offset += button_height + margin_y

    # --- Tombol Lock ---
    rect_start = (panel_x_start + (panel_width - button_main_width) // 2, current_y_offset)
    rect_end = (rect_start[0] + button_main_width, current_y_offset + button_height)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BUTTON_BG, -1)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
    put_text_with_icon(img, "Lock", icon_lock, rect_start[0], (rect_start[1] + rect_end[1]) // 2, button_height)
    current_y_offset += button_height + margin_y

    # --- Tombol Menu ---
    rect_start = (panel_x_start + (panel_width - button_main_width) // 2, current_y_offset)
    rect_end = (rect_start[0] + button_main_width, current_y_offset + button_height)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BUTTON_BG, -1)
    cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
    put_text_with_icon(img, "Menu", icon_menu, rect_start[0], (rect_start[1] + rect_end[1]) // 2, button_height)
    current_y_offset += button_height + margin_y * 3 # Jarak lebih besar sebelum Standby

    # --- Tombol Standby ---
    rect_start = (panel_x_start + (panel_width - button_main_width) // 2, current_y_offset)
    rect_end = (rect_start[0] + button_main_width, current_y_offset + button_height)
    cv2.rectangle(img, rect_start, rect_end, COLOR_STANDBY, -1)
    cv2.rectangle(img, rect_start, rect_end, COLOR_WHITE, 2)
    put_text_with_icon(img, "Standby", icon_standby, rect_start[0], (rect_start[1] + rect_end[1]) // 2, button_height)

# Fungsi yang sudah direvisi
def bottom_panel_revised(img, parameters):
    # if len(parameters) >= 5:
    #     raise ValueError("Fungsi ini membutuhkan tepat 5 parameter dalam list.")

    panel_x_end = W - 184
    panel_y_start = H - 125
    panel_height = 125

    # --- Background Panel Utama ---
    # Gambar background gelap untuk seluruh area tombol
    cv2.rectangle(img, (0, panel_y_start), (panel_x_end, panel_y_start + panel_height), COLOR_MAIN_PANEL_BG, -1)
    
    panel_y_start = H - 90
    panel_height = 90
    
    # --- Background Panel Parameter ---
    cv2.rectangle(img, (0, panel_y_start), (panel_x_end, panel_y_start + panel_height), COLOR_GRAY_BG, -1)
    cv2.line(img, (0, panel_y_start), (0, H), COLOR_BORDER, 1) # Garis pembatas vertikal

    # --- Membuat 6 Kotak untuk Parameter ---
    panel_item_x_start = 10
    panel_item_width = 100
    button_height = 75  # Tinggi kotak parameter disesuaikan
    margin_y = (panel_height - button_height) // 2
    current_y_offset = panel_y_start + margin_y

    for i in range(6):
        rect_start = (panel_item_x_start + i * panel_item_width, current_y_offset)
        rect_end = (rect_start[0] + panel_item_width - 10, current_y_offset + button_height)
        
        # Gambar kotak background
        cv2.rectangle(img, rect_start, rect_end, COLOR_LIGHT_GRAY_BG, -1)
        cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)

        box_width = panel_item_width - 10

        # Logika untuk 5 parameter pertama (dinamis)
        if i < 5:
            label, value, unit = parameters[i]

            # --- 1. Teks Label (Atas) ---
            label_size = cv2.getTextSize(label, FONT_SMALL_Bottom, 0.4, 1)[0]
            label_x = rect_start[0] + (box_width - label_size[0]) // 2
            label_y = rect_start[1] + 15
            cv2.putText(img, label, (label_x, label_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)

            # --- 2. Teks Nilai (Tengah) ---
            value_size = cv2.getTextSize(value, FONT_LARGE, 1.2, 2)[0]
            value_x = rect_start[0] + (box_width - value_size[0]) // 2
            value_y = rect_start[1] + (button_height + value_size[1]) // 2 - 5 # Sedikit ke atas
            cv2.putText(img, value, (value_x, value_y), FONT_LARGE, 1.2, COLOR_WHITE, 2, cv2.LINE_AA)

            # --- 3. Teks Unit (Bawah) ---
            unit_size = cv2.getTextSize(unit, FONT_SMALL_Bottom, 0.4, 1)[0]
            unit_x = rect_start[0] + (box_width - unit_size[0]) // 2
            unit_y = rect_end[1] - 8
            cv2.putText(img, unit, (unit_x, unit_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)

        # Logika untuk kotak keenam (statis)
        else:
            arrow_text = ">>"
            arrow_size = cv2.getTextSize(arrow_text, FONT_LARGE, 1, 2)[0]
            arrow_x = rect_start[0] + (box_width - arrow_size[0]) // 2
            arrow_y = rect_start[1] + (button_height + arrow_size[1]) // 2
            cv2.putText(img, arrow_text, (arrow_x, arrow_y), FONT_LARGE, 1, COLOR_WHITE, 2, cv2.LINE_AA)
            
    return img




def mid_panel(img,parameters_data=None):
    
    panel_x_end = W - 184
    panel_y_start =  100
    panel_height = 485      
    # --- Background Panel Utama ---

    cv2.rectangle(img, (0, panel_y_start), (panel_x_end, panel_y_start + panel_height), COLOR_MAIN_PANEL_BG, -1)
    panel_y_start = panel_y_start + 35
    panel_height = 450
    # Gambar background gray untuk seluruh area tombol
    cv2.rectangle(img, (0, panel_y_start), (panel_x_end, panel_y_start + panel_height), COLOR_GRAY_BG, -1)

    # --- grafik ---
    panel_x_start = 10
    panel_width = 725

    panel_y_start = panel_y_start + 10
    panel_height = 430

    cv2.rectangle(img, (panel_x_start, panel_y_start), (panel_x_start + panel_width, panel_y_start + panel_height), COLOR_BACKGROUND, -1)
    # --- item ---
    panel_x_start = panel_x_start + panel_width + 10
    panel_width = 340

    panel_y_start = panel_y_start
    panel_height = 430

    cv2.rectangle(img, (panel_x_start, panel_y_start), (panel_x_start + panel_width, panel_y_start + panel_height), COLOR_BACKGROUND, -1)
    

    
    cv2.line(img, (panel_x_start + panel_width//2, panel_y_start), (panel_x_start + panel_width//2, panel_y_start + panel_height), COLOR_BORDER, 1) # Garis pembatas vertikal


    for i in range(0,3):
        if i > 0:
            cv2.line(img, (panel_x_start, panel_y_start + i*panel_height//3), (panel_x_start + panel_width//2, panel_y_start + i*panel_height//3), COLOR_BORDER, 1) # Garis pembatas horizontal
        # text kiri atas
        label = parameter_data[i][0]
        label_size = cv2.getTextSize(label, FONT_SMALL_Bottom, 0.4, 1)[0]
        label_x = panel_x_start + 10
        label_y = panel_y_start + i*panel_height//3 + 20
        cv2.putText(img, label, (label_x, label_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)
        # text kiri tengah
        label = parameter_data[i][2]
        label_size = cv2.getTextSize(label, FONT_SMALL_Bottom, 0.4, 1)[0]
        label_x = panel_x_start + 10
        label_y = panel_y_start + i*panel_height//3 + 40
        cv2.putText(img, label, (label_x, label_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)
        # text value tengah
       
        label = parameter_data[i][1]
        label_size = cv2.getTextSize(label, FONT_LARGE, 2, 2)[0]
        label_x = panel_x_start + 10
        label_y = panel_y_start + i*panel_height//3 + 115
        # justivasi kanan
        label_width = cv2.getTextSize(label, FONT_LARGE, 2, 2)[0][0]
        label_x = panel_x_start + panel_width//2 - label_width - 25


        cv2.putText(img, label, (label_x, label_y), FONT_LARGE, 2, COLOR_WHITE, 2, cv2.LINE_AA)

    for i in range(0,6):
        if i > 0:
            cv2.line(img, (panel_x_start + panel_width//2, panel_y_start + i*panel_height//6), (panel_x_start + panel_width, panel_y_start + i*panel_height//6), COLOR_BORDER, 1) # Garis pembatas horizontal

        # text kiri atas
        label = parameter_data[i+3][0]
        label_size = cv2.getTextSize(label, FONT_SMALL_Bottom, 0.4, 1)[0]
        label_x = panel_x_start + panel_width//2 + 10
        label_y = panel_y_start + i*panel_height//6 + 20
        cv2.putText(img, label, (label_x, label_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)
        # text kiri tengah
        label = parameter_data[i+3][2]
        label_size = cv2.getTextSize(label, FONT_SMALL_Bottom, 0.4, 1)[0]
        label_x = panel_x_start + panel_width//2 + 10
        label_y = panel_y_start + i*panel_height//6 + 40
        cv2.putText(img, label, (label_x, label_y), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)
        # text value tengah
        label = parameter_data[i+3][1]
        label_size = cv2.getTextSize(label, FONT_LARGE, 1, 2)[0]
        label_x = panel_x_start + panel_width//2 + 10   
        label_y = panel_y_start + i*panel_height//6 + 50
        # justivasi kanan
        label_width = cv2.getTextSize(label, FONT_LARGE, 1, 2)[0][0]
        label_x = panel_x_start + panel_width - label_width - 25
        cv2.putText(img, label, (label_x, label_y), FONT_LARGE, 1, COLOR_WHITE, 2, cv2.LINE_AA)

    return img

# --- Data Parameter (Diperlukan untuk membuat grafik proporsional) ---
# Mengambil nilai numerik dari parameter yang relevan untuk grafik
Ppeak_val = 23
TVe_val = 518
ftotal_val = 12
PEEP_val = 4.9

# --- Fungsi untuk Menggambar Grafik Ventilator (Dinamis dengan Cosinus) ---
def draw_waveforms_dynamic(img, x_start, y_start, width, height, t_offset=0, freq=12, Ppeak=Ppeak_val, PEEP=PEEP_val, TVe=TVe_val):

    
    # Label Waveforms
    h_per_graph = height // 3 
    
    cv2.putText(img, "Paw cmH2O", (x_start + 10, y_start + 20 ), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)
    cv2.putText(img, "Flow L/min", (x_start + 10, y_start + h_per_graph +20 ), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)
    cv2.putText(img, "Volume mL", (x_start + 10, y_start + 2*h_per_graph +20), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)

    # Garis tengah/base (misalnya untuk Flow/Volume nol)
    cv2.line(img, (x_start, y_start + h_per_graph), (x_start + width, y_start + h_per_graph), COLOR_BORDER, 1)
    cv2.line(img, (x_start, y_start + 2*h_per_graph), (x_start + width, y_start + 2*h_per_graph), COLOR_BORDER, 1)

    # --- Parameter Dinamis ---
    T_cycle = 60.0 / freq # Periode siklus pernapasan (misalnya 60/12 = 5 detik)
    Insp_time = 1.70      # Waktu inspirasi (diambil dari parameter)
    Exp_time = T_cycle - Insp_time # Waktu ekspirasi

    # Amplitudo visual (dalam piksel)
    amp_P = 50 
    amp_V = 45 
    amp_F = 40 

    # Titik-titik grafik
    points_P = []
    points_F = []
    points_V = []
    
    # Skala Waktu (X-axis)
    time_scale_factor = width / T_cycle / 3 # Skalakan 3 siklus agar terlihat di layar
    
    for x_pixel in range(width):
        # Waktu yang diwakili oleh piksel x (relatif terhadap t_offset)
        t_global = (x_pixel / width) * (3 * T_cycle) + t_offset
        t_relative = t_global % T_cycle # Waktu di dalam siklus saat ini
        
        # --- 1. Grafik Tekanan (Paw) ---
        y_P_base = (y_start + h_per_graph//2) + 15
        if t_relative < Insp_time:
            # Inspirasi: Tekanan naik dari PEEP ke Ppeak
            # Menggunakan cosinus untuk kurva yang lebih alami
            t_norm = t_relative / Insp_time
            P = PEEP_val + (Ppeak_val - PEEP_val) * (1 - math.cos(math.pi * t_norm)) / 2
            y_P = y_P_base - (P - PEEP_val) * (amp_P / (Ppeak_val - PEEP_val))
        else:
            # Ekspirasi: Tekanan kembali ke PEEP
            t_norm = (t_relative - Insp_time) / Exp_time
            y_P = y_P_base + amp_P * math.sin(math.pi * t_norm) * 0.1 # Kurva ekspirasi kecil
        
        points_P.append((x_start + x_pixel, int(y_P)))

        # --- 2. Grafik Volume ---
        y_V_base = (y_start + 2*h_per_graph + h_per_graph//2) + 15
        if t_relative < Insp_time:
            # Inspirasi: Volume naik dari 0 ke TVe
            t_norm = t_relative / Insp_time
            V = TVe_val * (1 - math.cos(math.pi * t_norm)) / 2
        else:
            # Ekspirasi: Volume turun dari TVe kembali ke 0
            t_norm = (t_relative - Insp_time) / Exp_time
            V = TVe_val * (1 - t_norm**2) # Fungsi kuadratik untuk kurva ekspirasi cepat

        y_V = y_V_base - V * (amp_V / TVe_val)
        points_V.append((x_start + x_pixel, int(y_V)))

        # --- 3. Grafik Aliran (Flow) ---
        y_F_base = (y_start + h_per_graph + h_per_graph//2) + 15
        if t_relative < Insp_time:
            # Inspirasi: Aliran positif (mirip kotak/persegi)
            F = amp_F # Aliran konstan (simulasi PCV/VCV)
        else:
            # Ekspirasi: Aliran negatif (kembali ke nol)
            t_norm = (t_relative - Insp_time) / Exp_time
            F = -amp_F * math.sin(math.pi * (1-t_norm)) # Aliran ekspirasi
            if t_norm > 0.8: # Potongan aliran cepat mendekati nol
                 F *= (1 - t_norm) / 0.2
            
        y_F = y_F_base - F
        points_F.append((x_start + x_pixel, int(y_F)))
            
    # Menggambar garis
    points_P_np = np.array(points_P, np.int32).reshape((-1, 1, 2))
    cv2.polylines(img, [points_P_np], False, COLOR_ORANGE, 2)
    
    points_F_np = np.array(points_F, np.int32).reshape((-1, 1, 2))
    cv2.polylines(img, [points_F_np], False, COLOR_BLUE, 2)
    
    points_V_np = np.array(points_V, np.int32).reshape((-1, 1, 2))
    cv2.polylines(img, [points_V_np], False, COLOR_BLUE, 2)
    
    return img






# --- FUNGSI BARU: PERHITUNGAN PARAMETER DINAMIS ---
def calculate_dynamic_params(t_global, initial_params, Ppeak_val=Ppeak_val, TVe_val=TVe_val, FTOTAL_SET=ftotal_val, TINS_SET= TVe_val, PEEP_SET=PEEP_val, IBW_VAL=70):
    """
    Menghitung parameter dinamis berdasarkan waktu simulasi (t_global)
    dan parameter yang diatur.
    """
    
    # Ambil parameter yang diatur dari list inisial (disimpan sebagai string)
    # Ini harusnya diambil dari input user di aplikasi nyata, tapi kita gunakan konstanta.
    
    # Konstanta untuk perhitungan kurva kosinus
    T_cycle = 60.0 / FTOTAL_SET
    Insp_time = TINS_SET
    Exp_time = T_cycle - Insp_time
    
    t_relative = t_global % T_cycle
    
    # --- RUMUS DINAMIS 1: Simulasi Puncak $P_{peak}$ dan $T_{Ve}$ ---
    # Kita akan mensimulasikan nilai $P_{peak}$ dan $T_{Ve}$ secara sinusoidal
    # agar terlihat "bernafas" dan sedikit bising/berfluktuasi.
    
    # Puncak $P_{peak}$: Tekanan akan mencapai puncak mendekati akhir Inspirasi
    if t_relative < Insp_time:
        t_norm = t_relative / Insp_time
        # Simulasi Tekanan (seperti di fungsi draw_waveforms_dynamic)
        P_measured = PEEP_SET + (Ppeak_val - PEEP_SET) * (1 - math.cos(math.pi * t_norm)) / 2
        
        # Simulasi Volume
        V_measured = TVe_val * (1 - math.cos(math.pi * t_norm)) / 2
    else:
        # Ekspirasi
        P_measured = PEEP_SET
        V_measured = 0 # Asumsi Volume kembali ke nol
        
    # Tambahkan sedikit "noise" (fluktuasi) pada $T_{Ve}$ yang diukur
    # TVe akan menjadi nilai puncak siklus. Kita ambil nilai maksimum per siklus.
    # Namun, karena ini dijalankan per frame, kita akan membulatkan nilai V_measured saat mencapai puncak.
    
    # Untuk simulasi sederhana, mari kita buat nilai dinamis hanya berfluktuasi 
    # di sekitar nilai setpoint saat mencapai puncak siklus.
    
    TVe_MEASURED = TVe_val + (random.uniform(-10, 10)) # Fluktuasi kecil di sekitar 518
    Ppeak_MEASURED = Ppeak_val + (random.uniform(-0.5, 0.5)) # Fluktuasi kecil di sekitar 23

    # --- RUMUS DINAMIS 2: Pmean (Mean Airway Pressure) ---
    # Pmean dihitung sebagai area di bawah kurva Paw dibagi waktu siklus.
    # Untuk simplifikasi simulasi: Pmean = (Ppeak + PEEP) / 2 * (Ti/Ttotal) + PEEP * (Te/Ttotal)
    # Di ventilator nyata, Pmean ~ (Ppeak * $T_i$ + PEEP * $T_e$) / $T_{total}$
    Pmean_MEASURED = (Ppeak_MEASURED * Insp_time + PEEP_SET * Exp_time) / T_cycle
    
    # --- RUMUS DINAMIS 3: MVe (Minute Volume) ---
    # MVe = TVe * $f_{total}$ (diukur, bukan diatur)
    MVe_MEASURED = TVe_MEASURED * FTOTAL_SET / 1000 # Bagi 1000 karena $T_{Ve}$ dalam mL
    
    # --- RUMUS DINAMIS 4: $f_{spn}$ (Spontaneous Rate) ---
    # Kita simulasikan fspn aktif hanya kadang-kadang (misalnya setiap 5 detik)
    fspn_MEASURED = 0
    if (t_global // 5) % 2 == 1:
        fspn_MEASURED = 0 # Pasien istirahat
    else:
        fspn_MEASURED = 2 # Pasien mengambil 2 napas spontan dalam interval ini
        
    # --- RUMUS DINAMIS 5: $T_{Ve}/IBW$ ---
    # $T_{Ve}/IBW = T_{Ve}$ / Berat Ideal (IBW)
    TVe_IBW_MEASURED = TVe_MEASURED / IBW_VAL
    
    # --- UPDATE LIST PARAMETER ---
    new_params = initial_params[:] # Salin list
    
    # Update Nilai Dinamis (indeks dalam parameter_data):
    # TVe (index 1)
    new_params[1] = (new_params[1][0], f"{TVe_MEASURED:.0f}", new_params[1][2])
    # Ppeak (index 5)
    new_params[5] = (new_params[5][0], f"{Ppeak_MEASURED:.1f}", new_params[5][2])
    # Pmean (index 6)
    new_params[6] = (new_params[6][0], f"{Pmean_MEASURED:.1f}", new_params[6][2])
    # MVe (index 7)
    new_params[7] = (new_params[7][0], f"{MVe_MEASURED:.2f}", new_params[7][2])
    # fspn (index 8)
    new_params[8] = (new_params[8][0], f"{fspn_MEASURED:.0f}", new_params[8][2])
    # TVe/IBW (index 9)
    new_params[9] = (new_params[9][0], f"{TVe_IBW_MEASURED:.1f}", new_params[9][2])

    return new_params

# ... (Sisipkan kembali fungsi draw_waveforms_dynamic, mid_panel, bottom_panel_revised, dll. yang menggunakan nilai Ppeak_val, TVe_val, ftotal_val, PEEP_val) ...
# Catatan: Karena $P_{peak}$, $T_{Ve}$, $f_{total}$, $P_{EEP}$ di fungsi grafik awalnya adalah konstanta global, 
# Anda perlu memastikan fungsi grafik diperbarui untuk menggunakan nilai dinamis yang dihitung di atas 
# jika Anda ingin grafik mencerminkan fluktuasi parameter dinamis.
# Untuk sementara, mari kita biarkan fungsi grafik menggunakan konstanta default agar kode ini dapat berjalan.


# --- PROGRAM UTAMA YANG DIPERBARUI ---
if __name__ == "__main__":
    # Inisialisasi parameter_data awal
    parameter_data = [
        ("FiO2", "21", "vol %"),
        ("TVe", "518", "mL"),
        ("ftotal", "12", "/min"),
        ("Insp", "1.70", "s"),
        ("PEEP", "4.9", "cmH2O"),
        ("Ppeak", "23", "cmH2O"),
        ("Pmean", "9.2", "cmH2O"),
        ("MVe", "6.23", "L/min"),
        ("fspn", "0", "/min"),
        ("TVe/IBW", "7.4", "mL/kg")
    ]
    
    # ... (Inisialisasi Window OpenCV) ...
    cv2.namedWindow("Ventilator Simulator", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Ventilator Simulator", W, H)
    
    t = 0
    fps = 60 # Frame per second
    delay = int(1000 / fps)
    
    # Nilai awal konstanta yang dipakai di grafik (HARUS SAMA DENGAN NILAI DEFAULT)
    Ppeak_val = 19.0
    TVe_val = 518.0

    while True:
        # --- LOKASI RUMUS DINAMIS: Dipanggil di setiap frame ---
        # 1. Hitung parameter dinamis baru
        new_parameter_data = calculate_dynamic_params(t, parameter_data)
        
        # 2. Update parameter_data yang akan ditampilkan
        parameter_data = new_parameter_data
        
        # 3. Update nilai konstanta yang digunakan di dalam fungsi draw_waveforms_dynamic
        # Agar grafik juga merefleksikan perubahan (walaupun hanya fluktuasi kecil)
        TVe_val = float(parameter_data[1][1]) # Ambil nilai TVe yang sudah difluktuasi
        Ppeak_val = float(parameter_data[5][1]) # Ambil nilai Ppeak yang sudah difluktuasi
        
        # --- Menggambar UI ---
        background = np.zeros((H, W, 3), dtype=np.uint8)
        background[:] = COLOR_BACKGROUND
        
        draw_right_panel_revised(background)
        bottom_panel_revised(background, parameter_data) # Menggunakan data baru
        mid_panel(background, parameter_data) # Menggunakan data baru
        
        canvas = background
        
        # Replikasi struktur panel utama untuk mendapatkan koordinat grafik
        panel_y_start = 100 + 35 
        graph_x_start = 10
        graph_width = 725
        graph_y_start = panel_y_start + 10
        graph_height = 430
        
        # 1. Gambar background grafik
        cv2.rectangle(canvas, (graph_x_start, graph_y_start), (graph_x_start + graph_width, graph_y_start + graph_height), COLOR_BACKGROUND, -1)
        
        # 2. Gambar Waveforms Dinamis
        # Menggunakan parameter global Ppeak_val dan TVe_val yang sudah di-update
        # untuk menggambar kurva yang sedikit berfluktuasi
        canvas = draw_waveforms_dynamic(canvas, graph_x_start, graph_y_start, graph_width, graph_height, t_offset=t, freq=float(parameter_data[2][1]), Ppeak=Ppeak_val, PEEP=float(parameter_data[4][1]), TVe=TVe_val)
        
        cv2.imshow("Ventilator Simulator", background)
        
        # Update waktu (dinamis)
        t += (1.0 / fps) * 0.5 # Kecepatan pergerakan 0.5x kecepatan real-time

        if cv2.waitKey(delay) & 0xFF == 27:
            break

    cv2.destroyAllWindows()