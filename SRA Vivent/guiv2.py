import cv2
import numpy as np
import math
import time


# ========Dummy data flow untuk grafik========
MAX_POINTS = 100          # jumlah titik di layar
flow_buffer = [0] * MAX_POINTS

start_time = time.time()

def get_flow_value():
    t = time.time() - start_time
    return 60 * math.sin(2 * math.pi * t / 4)  # napas ~4 detik




# --- KONFIGURASI WARNA (Format BGR) ---
# Warna diambil sampelnya mendekati gambar asli
COLOR_BG_MAIN = (235, 235, 235)   # Abu-abu terang untuk area tengah
COLOR_BG_LEFT = (139, 111, 96)      # Biru tua untuk menu kiri
COLOR_BG_TOP = (204, 144, 119)    # Biru sedang untuk header atas
COLOR_BG_BOTTOM = (233, 168, 48)  # Biru terang untuk tombol bawah (Cyan-ish)
COLOR_TEXT_WHITE = (255, 255, 255)
COLOR_TEXT_DARK = (50, 50, 50)
COLOR_BATTERY_GREEN = (50, 200, 50)
COLOR_SEPARATOR = (255, 255, 255)

# --- KONFIGURASI DIMENSI ---
WIDTH = 800
HEIGHT = 480
LEFT_MENU_WIDTH = 160
TOP_BAR_HEIGHT = 50
BOTTOM_BAR_HEIGHT = 60
FONT = cv2.FONT_HERSHEY_SIMPLEX
COLOR_LEFT_ACTIVE = (61, 61, 68)  # BGR sesuai permintaan

active_bottom_view = "default"
active_left_index = -1
LEFT_MENU_PADDING_TOP = TOP_BAR_HEIGHT
LEFT_MENU_PADDING_BOTTOM = BOTTOM_BAR_HEIGHT + 20

def draw_gui():
    # 1. Buat kanvas kosong (gambar hitam)
    img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    # --- MENGGAMBAR AREA LATAR BELAKANG ---
    
    # Area Utama (Tengah)
    cv2.rectangle(img, (LEFT_MENU_WIDTH, TOP_BAR_HEIGHT), (WIDTH, HEIGHT - BOTTOM_BAR_HEIGHT), COLOR_BG_MAIN, -1)
    
    # Menu Kiri
    cv2.rectangle(img, (0, 0), (LEFT_MENU_WIDTH, HEIGHT), COLOR_BG_LEFT, -1)
    
    # Bar Atas
    cv2.rectangle(img, (LEFT_MENU_WIDTH, 0), (WIDTH, TOP_BAR_HEIGHT), COLOR_BG_TOP, -1)
    
    # Bar Bawah
    cv2.rectangle(img, (LEFT_MENU_WIDTH, HEIGHT - BOTTOM_BAR_HEIGHT), (WIDTH, HEIGHT), COLOR_BG_BOTTOM, -1)


    # --- MENAMBAHKAN TEKS & ELEMEN ---

    buttons_left = ["Airway", "Breath Views", "High Pressure", "Low Pressure", ""]

    menu_start_y = 0
    menu_end_y = HEIGHT - BOTTOM_BAR_HEIGHT
    btn_height = (menu_end_y - menu_start_y) // len(buttons_left)

    for i, text in enumerate(buttons_left):
        y1 = menu_start_y + i * btn_height
        y2 = y1 + btn_height

        # background aktif
        if i == active_left_index:
            cv2.rectangle(img, (0, y1), (LEFT_MENU_WIDTH, y2), COLOR_LEFT_ACTIVE, -1)

        # teks center vertikal
        text_size = cv2.getTextSize(text, FONT, 0.6, 1)[0]
        text_y = y1 + (btn_height + text_size[1]) // 2
        cv2.putText(img, text, (10, text_y), FONT, 0.6, COLOR_TEXT_WHITE, 1)

        # garis pemisah
        cv2.line(img, (0, y2), (LEFT_MENU_WIDTH, y2), COLOR_SEPARATOR, 1)

    # Tombol "Menus" di kiri bawah
    cv2.putText(img, "Menus", (40, HEIGHT - 20), FONT, 0.8, COLOR_TEXT_WHITE, 2)
   

    # 2. Konten Bar Atas (Header)
    header_title = "Airway Flow" if active_bottom_view == "flow" else "Airway / Graph"
    cv2.putText(img, header_title,
                (LEFT_MENU_WIDTH + 20, 35),
                FONT, 0.8, COLOR_TEXT_WHITE, 2)

    
    # Ikon Baterai & Plug (Simulasi sederhana dengan bentuk geometri)
    bat_x, bat_y = WIDTH - 50, 15
    bat_w, bat_h = 30, 15
    # Badan baterai
    cv2.rectangle(img, (bat_x, bat_y), (bat_x + bat_w, bat_y + bat_h), COLOR_TEXT_WHITE, 1)
    # Isi baterai (hijau)
    cv2.rectangle(img, (bat_x + 2, bat_y + 2), (bat_x + bat_w - 5, bat_y + bat_h - 2), COLOR_BATTERY_GREEN, -1)
    # Kutub baterai
    cv2.rectangle(img, (bat_x + bat_w, bat_y + 4), (bat_x + bat_w + 4, bat_y + bat_h - 4), COLOR_TEXT_WHITE, -1)
    
    # Ikon Plug (sangat sederhana)
    plug_x = WIDTH - 85
    cv2.rectangle(img, (plug_x, 20), (plug_x + 20, 30), COLOR_TEXT_WHITE, -1)
    cv2.line(img, (plug_x - 5, 22), (plug_x, 22), COLOR_TEXT_WHITE, 2)
    cv2.line(img, (plug_x - 5, 28), (plug_x, 28), COLOR_TEXT_WHITE, 2)


    # 3. Konten Area Utama (Tengah)
        # ===== KONTEN AREA UTAMA =====
    if active_bottom_view == "default":
        main_text = "Select the Airway function to graph:"
        text_size = cv2.getTextSize(main_text, FONT, 0.7, 2)[0]
        text_x = LEFT_MENU_WIDTH + (WIDTH - LEFT_MENU_WIDTH - text_size[0]) // 2
        text_y = TOP_BAR_HEIGHT + 100
        cv2.putText(img, main_text, (text_x, text_y), FONT, 0.7, COLOR_TEXT_DARK, 2)

    elif active_bottom_view == "flow":
        draw_airway_flow_view(img)

    # 4. Konten Bar Bawah (Tombol)
    buttons_bottom = ["Flow", "Pressure", "Volume", "Oxygen", "Cancel"]
    num_btns = len(buttons_bottom)
    btn_width = (WIDTH - LEFT_MENU_WIDTH) // num_btns
    
    for i, text in enumerate(buttons_bottom):
        x_start = LEFT_MENU_WIDTH + (i * btn_width)
        # Hitung posisi tengah untuk teks
        text_size = cv2.getTextSize(text, FONT, 0.7, 1)[0]
        text_x = x_start + (btn_width - text_size[0]) // 2
        text_y = HEIGHT - 25
        
        cv2.putText(img, text, (text_x, text_y), FONT, 0.7, COLOR_TEXT_WHITE, 1)
        
        # Gambar garis pemisah vertikal (kecuali setelah tombol terakhir)
        if i < num_btns - 1:
            cv2.line(img, (x_start + btn_width, HEIGHT - BOTTOM_BAR_HEIGHT), 
                     (x_start + btn_width, HEIGHT), COLOR_SEPARATOR, 1)

    return img


def draw_airway_flow_view(img):
    content_x = LEFT_MENU_WIDTH + 20

    # Nilai utama
    cv2.putText(img, "-0.01 lpm",
                (content_x, TOP_BAR_HEIGHT + 45),
                FONT, 1.2, (0, 0, 0), 3)
    
    cv2.putText(img, "MAX: 0.10",
                (LEFT_MENU_WIDTH + 20, TOP_BAR_HEIGHT + 90),
                FONT, 0.5, COLOR_TEXT_DARK, 1)
    cv2.putText(img, "MIN: -0.08",
                (LEFT_MENU_WIDTH + 140, TOP_BAR_HEIGHT + 90),
                FONT, 0.5, COLOR_TEXT_DARK, 1)
    cv2.putText(img, "AVG: 0.00",
                (LEFT_MENU_WIDTH + 280, TOP_BAR_HEIGHT + 90),
                FONT, 0.5, COLOR_TEXT_DARK, 1)


    # === ZOOM BUTTONS ===
    zoom_y = TOP_BAR_HEIGHT + 15
    zoom_w, zoom_h = 120, 35

    # Zoom IN
    cv2.rectangle(img,
                  (WIDTH - 280, zoom_y),
                  (WIDTH - 160, zoom_y + zoom_h),
                  (200, 200, 200), -1)
    cv2.putText(img, "Zoom IN +",
                (WIDTH - 270, zoom_y + 25),
                FONT, 0.5, COLOR_TEXT_DARK, 1)

    # Zoom OUT
    cv2.rectangle(img,
                  (WIDTH - 150, zoom_y),
                  (WIDTH - 30, zoom_y + zoom_h),
                  (200, 200, 200), -1)
    cv2.putText(img, "Zoom OUT -",
                (WIDTH - 145, zoom_y + 25),
                FONT, 0.5, COLOR_TEXT_DARK, 1)
    
        # === GRAPH AREA ===
    gx1 = content_x
    gy1 = TOP_BAR_HEIGHT + 120
    gx2 = WIDTH - 20
    gy2 = HEIGHT - BOTTOM_BAR_HEIGHT - 20

    # Frame grafik
    cv2.rectangle(img, (gx1, gy1), (gx2, gy2), (160, 160, 160), 1)

    axis_x = gx1 + 40
    axis_y = (gy1 + gy2) // 2

    # Axis Y
    cv2.line(img, (axis_x, gy1), (axis_x, gy2), COLOR_TEXT_DARK, 1)

    # Axis X (0 flow)
    cv2.line(img, (axis_x, axis_y), (gx2, axis_y), COLOR_TEXT_DARK, 1)

    # Y labels
    cv2.putText(img, "100", (gx1 + 5, gy1 + 15), FONT, 0.4, COLOR_TEXT_DARK, 1)
    cv2.putText(img, "0", (gx1 + 15, axis_y + 5), FONT, 0.4, COLOR_TEXT_DARK, 1)
    cv2.putText(img, "-100", (gx1 + 5, gy2 - 5), FONT, 0.4, COLOR_TEXT_DARK, 1)


    # === X Labels (seconds) ===
    for i in range(6):
        x = axis_x + i * (gx2 - axis_x) // 5
        cv2.putText(img, f"{i*2}",
                    (x - 5, gy2 - 10),
                    FONT, 0.4, COLOR_TEXT_DARK, 1)

    cv2.putText(img, "s",
                (gx2 - 10, gy2 - 10),
                FONT, 0.4, COLOR_TEXT_DARK, 1)


       # === REALTIME SCROLLING GRAPH ===
    prev_point = None

    for i, value in enumerate(flow_buffer):
        x = axis_x + i * (gx2 - axis_x) // (MAX_POINTS - 1)
        y = map_value_to_y(value, gy1, gy2)

        if prev_point is not None:
            cv2.line(img, prev_point, (x, y), (40, 40, 40), 2)

        prev_point = (x, y)






def map_value_to_y(value, gy1, gy2):
    """
    value : data flow (-100 .. 100)
    gy1   : top grafik
    gy2   : bottom grafik
    """
    value = max(-100, min(100, value))  # clamp aman

    mid_y = (gy1 + gy2) // 2
    half_h = (gy2 - gy1) // 2

    # nilai +100 -> gy1, -100 -> gy2
    y = int(mid_y - (value / 100.0) * half_h)
    return y





# --- FUNGSI INTERAKSI MOUSE (OPSIONAL) ---
# Ini hanya untuk menunjukkan di mana Anda mengklik, 
# tidak membuat tombol benar-benar berfungsi secara native.
def mouse_callback(event, x, y, flags, param):
    global active_left_index, gui_image, active_bottom_view

    if event == cv2.EVENT_LBUTTONDOWN:

        # ===== LEFT MENU =====
        if x < LEFT_MENU_WIDTH and y < HEIGHT - BOTTOM_BAR_HEIGHT:
            btn_height = (HEIGHT - BOTTOM_BAR_HEIGHT) // 5
            index = y // btn_height
            if 0 <= index < 5:
                active_left_index = index

        # ===== BOTTOM BUTTONS =====
        if y > HEIGHT - BOTTOM_BAR_HEIGHT:
            btn_width = (WIDTH - LEFT_MENU_WIDTH) // 5
            index = (x - LEFT_MENU_WIDTH) // btn_width

            if index == 0:        # Flow
                active_bottom_view = "flow"
            else:
                active_bottom_view = "default"

        gui_image = draw_gui()




# --- MAIN LOOP ---
if __name__ == "__main__":
    # 1. Gambar GUI
    

    # 2. Buat jendela
    window_name = "Ventilator GUI Mockup (OpenCV)"
    cv2.namedWindow(window_name)
    
    # 3. Pasang fungsi callback mouse (untuk demo interaksi)
    cv2.setMouseCallback(window_name, mouse_callback)

    print("Tampilan GUI ventilator berhasil dibuat.")
    print("Klik di mana saja pada jendela untuk melihat koordinat di terminal.")
    print("Tekan tombol 'q' untuk keluar.")

    while True:
        # Tampilkan gambar
        # update flow buffer
        new_value = get_flow_value()
        flow_buffer.append(new_value)
        flow_buffer.pop(0)
        gui_image = draw_gui()

        cv2.imshow(window_name, gui_image)
        
        # Tunggu input keyboard (1ms delay)
        key = cv2.waitKey(1) & 0xFF
        
        # Jika 'q' ditekan, keluar loop
        if key == ord('q'):
            break

    cv2.destroyAllWindows()