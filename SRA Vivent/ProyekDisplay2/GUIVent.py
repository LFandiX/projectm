
import cv2
import numpy as np
import math
import datetime
import csv
import os
import traceback

# --- Konfigurasi dan Palet Warna ---
W, H = 1280, 720 # Ukuran window

# Warna yang digunakan (format BGR)
COLOR_BACKGROUND = (25, 25, 35)
COLOR_MAIN_PANEL_BG = (40, 40, 50)
COLOR_BUTTON_BG = (45, 45, 55)
COLOR_BORDER = (80, 80, 80)
COLOR_WHITE = (255, 255, 255)
COLOR_STANDBY = (25, 170, 255)
COLOR_GRAY_BG = (60, 60, 70)
COLOR_LIGHT_GRAY_BG = (90, 90, 100)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (255, 120, 0)
COLOR_ORANGE = (0, 165, 255)

# Font yang digunakan
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SMALL = cv2.FONT_HERSHEY_COMPLEX_SMALL
FONT_SMALL_Bottom = cv2.FONT_HERSHEY_SIMPLEX
FONT_LARGE = cv2.FONT_HERSHEY_DUPLEX

# --- Variabel Global untuk State ---
active_mid_panel_idx = 0
active_bottom_panel_idx = 0
show_vac_setup = False
setup_button_rects = [] # Untuk menyimpan area klik tombol setup

# --- Palet Warna & Konstanta dari GUI_Setup.py ---
SETUP_COLOR_POPUP_BG = (230, 230, 230)
SETUP_COLOR_TEXT_MAIN = (0, 0, 0)
SETUP_COLOR_TEXT_UNIT = (90, 90, 90)
SETUP_COLOR_BUTTON = (200, 200, 200)
SETUP_COLOR_BORDER = (150, 150, 150)
SETUP_COLOR_VALUE_BOX = (255, 255, 255)
SETUP_COLOR_BLUE_HIGHLIGHT = (200, 100, 0)

# --- State untuk Parameter Setup V-A/C ---
setup_params = {
    "O2%":    {"value": 21,  "unit": "vol.%", "inc": 1, "min": 21, "max": 100, "format": "{:.0f}", "increment": 0},
    "TV":     {"value": 500, "unit": "mL",    "inc": 10,"min": 50, "max": 1500,"format": "{:.0f}", "increment": 0},
    "f":      {"value": 12,  "unit": "/min",  "inc": 1, "min": 1,  "max": 100, "format": "{:.0f}", "increment": 0},
    "Tinsp":  {"value": 1.70,"unit": "s",     "inc": 0.1,"min": 0.1,"max": 5,   "format": "{:.2f}", "increment": 0},
    "PEEP":   {"value": 5,   "unit": "cmH2O", "inc": 1, "min": 0,  "max": 30,  "format": "{:.0f}", "increment": 0},
    "Flow":   {"value": 20.0,"unit": "L/min", "inc": 0.5,"min": 5,  "max": 60,  "format": "{:.1f}", "increment": 0},
    "F-Trig": {"value": 2.0, "unit": "L/min", "inc": 0.1,"min": 0.5,"max": 10,  "format": "{:.1f}", "increment": 0}
}

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


# --- Fungsi Baca CSV ---
def get_latest_csv_data(filename="data_ventilator.csv"):
    latest_data = {}
    if not os.path.exists(filename):
        return None
    try:
        with open(filename, 'r', newline='') as f:
            all_lines = f.readlines()
            if not all_lines: return None
            last_line = all_lines[-1].strip()
            if not last_line and len(all_lines) > 1:
                last_line = all_lines[-2].strip()
            
            if not last_line: return None

            reader = csv.reader([last_line])
            row = next(reader)
            headers = ["Date","VT(e)","Ti","Te","RR","I:E","PEEP","PIP","O2","RSD_VT","RSD_RR","RSD_IE","RSD_PEEP","RSD_PIP","RSD_O2"]
            if len(row) != len(headers): return None # baris korup
            latest_data = dict(zip(headers, row))
    except Exception as e:
        # print(f"Error reading CSV: {e}") # Hapus print agar tidak spam
        return None
    return latest_data

# --- Fungsi Gambar UI ---
def top_panel(img):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    time = datetime.datetime.now().strftime("%H:%M")
    panel_x_end = W - 184
    cv2.putText(img, "Mindray SV800", (40, 50), FONT_LARGE, 0.7, COLOR_WHITE, 2, cv2.LINE_AA)
    cv2.putText(img, "Mechanical Ventilator", (40, 75), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)
    datetime_text = f"{date}   {time}"
    datetime_size = cv2.getTextSize(datetime_text, FONT_SMALL_Bottom, 0.6, 1)[0]
    cv2.putText(img, datetime_text, (panel_x_end - datetime_size[0] - 20, 60), FONT_SMALL_Bottom, 0.6, COLOR_WHITE, 1, cv2.LINE_AA)

def mid_panel_bar(img, onpanel=0):
    panel_y_start, panel_height = 100, 35
    panel = ["Waveforms", "Spirometry", "Values", "Big Numerics"]
    for i, label in enumerate(panel):
        rect_start = (i * 180, panel_y_start)
        rect_end = (rect_start[0] + 170, panel_y_start + panel_height)
        is_on = (i == onpanel)
        color = COLOR_GRAY_BG if is_on else COLOR_MAIN_PANEL_BG
        cv2.rectangle(img, rect_start, rect_end, color, -1)
        if not is_on: cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
        text = "..." if label == "More..." else label
        text_size = cv2.getTextSize(text, FONT_SMALL_Bottom, 0.5, 1)[0]
        cv2.putText(img, text, (rect_start[0] + (170 - text_size[0]) // 2, rect_start[1] + (panel_height + text_size[1]) // 2), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)

def bottom_panel_bar(img, onpanel=0):
    panel_y_start, panel_height = H - 125, 35
    panel = ["V-A/C", "P-A/C", "V-SIMV", "P-SIMV", "CPAP/PSV", "APRV", "AMV"]
    for i, label in enumerate(panel):
        rect_start = (i * 100, panel_y_start)
        rect_end = (rect_start[0] + 90, panel_y_start + panel_height)
        is_on = (i == onpanel)
        color = COLOR_GRAY_BG if is_on else COLOR_MAIN_PANEL_BG
        cv2.rectangle(img, rect_start, rect_end, color, -1)
        if not is_on: cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
        text_size = cv2.getTextSize(label, FONT_SMALL_Bottom, 0.5, 1)[0]
        cv2.putText(img, label, (rect_start[0] + (90 - text_size[0]) // 2, rect_start[1] + (panel_height + text_size[1]) // 2), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)

def draw_right_panel_revised(img):
    panel_x_start = W - 185  # Posisi X awal untuk panel (lebih ke kiri sedikit)
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


def bottom_panel_revised(img, parameters):
    global p_data
    panel_x_end = W - 184
    panel_y_start = H - 90
    panel_height = 90
    cv2.rectangle(img, (0, panel_y_start), (panel_x_end, H), COLOR_MAIN_PANEL_BG, -1)
    cv2.rectangle(img, (0, panel_y_start), (panel_x_end, panel_y_start + panel_height), COLOR_GRAY_BG, -1)
    item_w, item_h = 100, 75
    y_offset = panel_y_start + (panel_height - item_h) // 2
    param_map = {"FiO2": 2, "TVe": 5, "Ppeak": 0, "Insp": 9, "PEEP": 4}
    for i, key in enumerate(["FiO2", "TVe", "Ppeak", "Insp", "PEEP"]):
        rect_start = (10 + i * item_w, y_offset)
        rect_end = (rect_start[0] + item_w - 10, y_offset + item_h)
        cv2.rectangle(img, rect_start, rect_end, COLOR_LIGHT_GRAY_BG, -1)
        cv2.rectangle(img, rect_start, rect_end, COLOR_BORDER, 1)
        param_index = param_map.get(key)
        if param_index is None or param_index >= len(parameters): continue
        label, value, unit = parameters[param_index]
        box_w = item_w - 10
        label_size = cv2.getTextSize(label, FONT_SMALL_Bottom, 0.4, 1)[0]
        cv2.putText(img, label, (rect_start[0] + (box_w - label_size[0]) // 2, rect_start[1] + 15), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)
        value_size = cv2.getTextSize(value, FONT_LARGE, 1.2, 2)[0]
        cv2.putText(img, value, (rect_start[0] + (box_w - value_size[0]) // 2, rect_start[1] + (item_h + value_size[1]) // 2 - 5), FONT_LARGE, 1.2, COLOR_WHITE, 2, cv2.LINE_AA)
        unit_size = cv2.getTextSize(unit, FONT_SMALL_Bottom, 0.4, 1)[0]
        cv2.putText(img, unit, (rect_start[0] + (box_w - unit_size[0]) // 2, rect_end[1] - 8), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1, cv2.LINE_AA)

def mid_panel(img, parameters_data):
    panel_x_end = W - 184
    graph_area = (10, 145, 725, 430)
    data_area_x = graph_area[0] + graph_area[2] + 10
    data_area_w = panel_x_end - data_area_x
    cv2.rectangle(img, (0, 135), (panel_x_end, H - 130), COLOR_GRAY_BG, -1)
    cv2.rectangle(img, (graph_area[0], graph_area[1]), (graph_area[0] + graph_area[2], graph_area[1] + graph_area[3]), COLOR_BACKGROUND, -1)
    cv2.rectangle(img, (data_area_x, graph_area[1]), (data_area_x + data_area_w, graph_area[1] + graph_area[3]), COLOR_BACKGROUND, -1)
    param_map = {"Ppeak": 0, "MVe": 1, "FiO2": 2, "Pmean": 3, "PEEP": 4, "TVe": 5, "ftotal": 6, "fspn": 7, "TVe/IBW": 8, "Insp": 9}
    left_keys = ["Ppeak", "MVe", "FiO2"]
    for i, key in enumerate(left_keys):
        y_pos = graph_area[1] + i * (graph_area[3] // 3)
        label, value, unit = parameters_data[param_map[key]]
        cv2.putText(img, label, (data_area_x + 10, y_pos + 20), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1)
        cv2.putText(img, unit, (data_area_x + 10, y_pos + 40), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1)
        val_size = cv2.getTextSize(value, FONT_LARGE, 2, 2)[0]
        cv2.putText(img, value, (data_area_x + data_area_w // 2 - val_size[0] - 15, y_pos + 115), FONT_LARGE, 2, COLOR_WHITE, 2)
        if i > 0: cv2.line(img, (data_area_x, y_pos), (data_area_x + data_area_w // 2, y_pos), COLOR_BORDER, 1)
    right_keys = ["Pmean", "PEEP", "TVe", "ftotal", "fspn", "TVe/IBW"]
    for i, key in enumerate(right_keys):
        y_pos = graph_area[1] + i * (graph_area[3] // 6)
        label, value, unit = parameters_data[param_map[key]]
        cv2.putText(img, label, (data_area_x + data_area_w // 2 + 10, y_pos + 20), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1)
        cv2.putText(img, unit, (data_area_x + data_area_w // 2 + 10, y_pos + 40), FONT_SMALL_Bottom, 0.4, COLOR_WHITE, 1)
        val_size = cv2.getTextSize(value, FONT_LARGE, 1, 2)[0]
        cv2.putText(img, value, (data_area_x + data_area_w - val_size[0] - 15, y_pos + 60), FONT_LARGE, 1, COLOR_WHITE, 2)
        if i > 0: cv2.line(img, (data_area_x + data_area_w // 2, y_pos), (data_area_x + data_area_w, y_pos), COLOR_BORDER, 1)
    cv2.line(img, (data_area_x + data_area_w // 2, graph_area[1]), (data_area_x + data_area_w // 2, graph_area[1] + graph_area[3]), COLOR_BORDER, 1)

def draw_waveforms_dynamic(img, x_start, y_start, width, height, Ppeak_val, TVe_val, PEEP_val, t_offset=0, freq=12):
    if freq <= 0 or TVe_val <= 0: return img # Guard clause
    h_per_graph = height // 3
    cv2.putText(img, "Paw cmH2O", (x_start + 10, y_start + 20), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)
    cv2.putText(img, "Flow L/min", (x_start + 10, y_start + h_per_graph + 20), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)
    cv2.putText(img, "Volume mL", (x_start + 10, y_start + 2 * h_per_graph + 20), FONT_SMALL_Bottom, 0.5, COLOR_WHITE, 1, cv2.LINE_AA)
    cv2.line(img, (x_start, y_start + h_per_graph), (x_start + width, y_start + h_per_graph), COLOR_BORDER, 1)
    cv2.line(img, (x_start, y_start + 2 * h_per_graph), (x_start + width, y_start + 2 * h_per_graph), COLOR_BORDER, 1)
    T_cycle = 60.0 / freq
    Insp_time = 1.70
    amp_P, amp_V, amp_F = 50, 45, 40
    points_P, points_F, points_V = [], [], []
    for x_pixel in range(width):
        t_global = (x_pixel / width) * (3 * T_cycle) + t_offset
        t_relative = t_global % T_cycle
        y_P_base = (y_start + h_per_graph // 2) + 15
        p_diff = Ppeak_val - PEEP_val
        if t_relative < Insp_time:
            t_norm = t_relative / Insp_time
            P = PEEP_val + p_diff * (1 - math.cos(math.pi * t_norm)) / 2
            y_P = y_P_base - (P - PEEP_val) * (amp_P / p_diff) if p_diff != 0 else y_P_base
        else:
            t_norm = (t_relative - Insp_time) / (T_cycle - Insp_time)
            y_P = y_P_base + amp_P * math.sin(math.pi * t_norm) * 0.1
        points_P.append((x_start + x_pixel, int(y_P)))
        y_V_base = (y_start + 2 * h_per_graph + h_per_graph // 2) + 15
        if t_relative < Insp_time:
            V = TVe_val * (1 - math.cos(math.pi * t_relative / Insp_time)) / 2
        else:
            V = TVe_val * (1 - ((t_relative - Insp_time)/(T_cycle - Insp_time))**2)
        y_V = y_V_base - V * (amp_V / TVe_val)
        points_V.append((x_start + x_pixel, int(y_V)))
        y_F_base = (y_start + h_per_graph + h_per_graph // 2) + 15
        if t_relative < Insp_time: F = amp_F
        else: F = -amp_F * math.sin(math.pi * (1-((t_relative - Insp_time)/(T_cycle - Insp_time))))
        y_F = y_F_base - F
        points_F.append((x_start + x_pixel, int(y_F)))
    cv2.polylines(img, [np.array(points_P, np.int32)], False, COLOR_ORANGE, 2)
    cv2.polylines(img, [np.array(points_F, np.int32)], False, COLOR_BLUE, 2)
    cv2.polylines(img, [np.array(points_V, np.int32)], False, COLOR_BLUE, 2)
    return img

def draw_setup_value_box(img, x, y, w, h, param_name, value, unit):
    cv2.rectangle(img, (x, y), (x + w, y + h), SETUP_COLOR_VALUE_BOX, -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), SETUP_COLOR_BORDER, 1)
    param_size = cv2.getTextSize(param_name, FONT, 0.7, 1)[0]
    cv2.putText(img, param_name, (x + (w - param_size[0]) // 2, y + 25), FONT, 0.7, SETUP_COLOR_TEXT_MAIN, 1)
    val_size = cv2.getTextSize(str(value), FONT, 1.2, 2)[0]
    cv2.putText(img, str(value), (x + (w - val_size[0]) // 2, y + h - 25), FONT, 1.2, SETUP_COLOR_TEXT_MAIN, 2)
    if unit:
        unit_size = cv2.getTextSize(unit, FONT, 0.6, 1)[0]
        cv2.putText(img, unit, (x + w - unit_size[0] - 5, y + h - 10), FONT, 0.6, SETUP_COLOR_TEXT_UNIT, 1)

def draw_setup_plus_minus_button(img, x, y, w, h, text):
    cv2.rectangle(img, (x, y), (x + w, y + h), SETUP_COLOR_BUTTON, -1)
    cv2.rectangle(img, (x, y), (x + w, y + h), SETUP_COLOR_BORDER, 1)
    text_size = cv2.getTextSize(text, FONT, 0.9, 2)[0]
    cv2.putText(img, text, (x + (w - text_size[0]) // 2, y + (h + text_size[1]) // 2), FONT, 0.9, SETUP_COLOR_TEXT_MAIN, 2)

def draw_vac_setup_popup(img):
    global setup_button_rects
    setup_button_rects.clear()
    POPUP_W, POPUP_H = 1100, 600
    POPUP_X, POPUP_Y = 0, H - POPUP_H
    overlay = img.copy()
    cv2.rectangle(overlay, (0, 0), (W, H), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.8, img, 1 - 0.8, 0, img)
    cv2.rectangle(img, (POPUP_X, POPUP_Y), (POPUP_X + POPUP_W, POPUP_Y + POPUP_H), SETUP_COLOR_POPUP_BG, -1)
    cv2.rectangle(img, (POPUP_X, POPUP_Y), (POPUP_X + POPUP_W, POPUP_Y + 70), (190, 190, 190), -1)
    cv2.putText(img, "V-A/C Setup", (POPUP_X + 20, POPUP_Y + 45), FONT, 1, SETUP_COLOR_TEXT_MAIN, 2)
    BOX_W, BOX_H = 120, 100
    BTN_PM_W, BTN_PM_H = 30, 30
    H_GAP, V_GAP = 20, 30
    start_x, start_y = POPUP_X + 20, POPUP_Y + 130
    current_x, current_y = start_x, start_y
    items_in_row = 0
    for key, p in setup_params.items():
        if items_in_row >= 4 and key != "F-Trig":
            current_x, current_y = start_x, current_y + BOX_H + V_GAP
            items_in_row = 0
        if key == "F-Trig":
             current_x, current_y = start_x, start_y + BOX_H + V_GAP
             items_in_row = 0
        
        minus_btn_rect = (current_x, current_y + (BOX_H - BTN_PM_H) // 2, BTN_PM_W, BTN_PM_H)
        draw_setup_plus_minus_button(img, *minus_btn_rect, "-")
        setup_button_rects.append(("param", key, "dec", minus_btn_rect))
        val_box_x = current_x + BTN_PM_W + 5
        formatted_value = p["format"].format(p["value"])
        draw_setup_value_box(img, val_box_x, current_y, BOX_W, BOX_H, key, formatted_value, p["unit"])
        plus_btn_rect = (val_box_x + BOX_W + 5, current_y + (BOX_H - BTN_PM_H) // 2, BTN_PM_W, BTN_PM_H)
        draw_setup_plus_minus_button(img, *plus_btn_rect, "+")
        setup_button_rects.append(("param", key, "inc", plus_btn_rect))
        current_x = plus_btn_rect[0] + BTN_PM_W + H_GAP
        items_in_row += 1
    BTN_BOTTOM_W, BTN_BOTTOM_H = 100, 40
    BOTTOM_Y = POPUP_Y + POPUP_H - BTN_BOTTOM_H - 20

    BTN_OK_RECT = (POPUP_X + POPUP_W - BTN_BOTTOM_W - 20, BOTTOM_Y, BTN_BOTTOM_W, BTN_BOTTOM_H)
  
    draw_setup_plus_minus_button(img, *BTN_OK_RECT, "Ok")

    setup_button_rects.append(("action", "ok", "exec", BTN_OK_RECT))

def mouse_callback(event, x, y, flags, param):

    global active_mid_panel_idx, active_bottom_panel_idx, show_vac_setup, p_data,param_increments

    if event == cv2.EVENT_LBUTTONDOWN:

        if show_vac_setup:

            for type, key, action, rect in setup_button_rects:

                if rect[0] <= x <= rect[0] + rect[2] and rect[1] <= y <= rect[1] + rect[3]:

                    if type == "action":

                        if key in ["ok"]: show_vac_setup = False

                    elif type == "param":

                        p = setup_params[key]

                        if action == "inc": 
                            p["value"] = min(p["max"], p["value"] + p["inc"])
                            p['increment'] += p.get('inc')

                        elif action == "dec": 
                            p["value"] = max(p["min"], p["value"] - p["inc"])
                            p['increment'] -= p.get('inc')
                        return

        else:

            if 100 <= y <= 135: active_mid_panel_idx = x // 180

            elif H - 125 <= y <= H - 90:

                clicked_idx = x // 100

                if clicked_idx == 0: show_vac_setup = True

                else: active_bottom_panel_idx = clicked_idx

if __name__ == "__main__":
    cv2.namedWindow("Ventilator UI Final", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Ventilator UI Final", W, H)
    cv2.setMouseCallback("Ventilator UI Final", mouse_callback)
    t = 0
    fps = 60
    delay = int(1000 / fps)
    param_increments = {
    "Ppeak": 1,
    "MVe": 0.1,
    "FiO2": 1,
    "PEEP": 1,
    "TVe": 10,
    "ftotal": 1,
    "Insp": 0.1,
    # Parameter yang tidak bisa diubah tidak perlu ada di sini
}
    while True:
        # import time
        # time.sleep(1)
        try:
            background = np.zeros((H, W, 3), dtype=np.uint8)
            background[:] = COLOR_BACKGROUND
            latest_data = get_latest_csv_data()
            # DEBUG: Uncomment the line below to see raw CSV data in console
            print(f"Data from CSV: {latest_data}")
            p_data = {
                "Ppeak": "23", "MVe": "6.23", "FiO2": "21", "Pmean": "9.2", "PEEP": "4.9",
                "TVe": "518", "ftotal": "12", "fspn": "0", "TVe/IBW": "7.4", "Insp": "1.70"
            }
            if latest_data:
                try:
                    p_data["Ppeak"] = f"{float(latest_data.get('PIP', p_data['Ppeak'])):.1f}"
                    p_data["FiO2"] = f"{(float(latest_data.get('O2', p_data['FiO2'])) + setup_params['O2%']['increment']):.0f}"
                    p_data["PEEP"] = f"{float(latest_data.get('PEEP', p_data['PEEP'])):.1f}"
                    p_data["TVe"] = f"{float(latest_data.get('VT(e)', p_data['TVe'])):.0f}"
                    p_data["ftotal"] = f"{float(latest_data.get('RR', p_data['ftotal'])):.1f}"
                    p_data["Insp"] = f"{float(latest_data.get('Ti', p_data['Insp'])):.2f}"
                    mve_val = (float(p_data["TVe"]) * float(p_data["ftotal"])) / 1000
                    p_data["MVe"] = f"{mve_val:.2f}"
                except (ValueError, TypeError) as e:
                    pass # Fail silently if data is corrupt, use defaults
            parameter_data = [
                ("Ppeak", p_data["Ppeak"], "cmH2O"), ("MVe", p_data["MVe"], "L/min"), ("FiO2", p_data["FiO2"], "vol %"),
                ("Pmean", p_data["Pmean"], "cmH2O"), ("PEEP", p_data["PEEP"], "cmH2O"), ("TVe", p_data["TVe"], "mL"),
                ("ftotal", p_data["ftotal"], "/min"), ("fspn", p_data["fspn"], "/min"), ("TVe/IBW", p_data["TVe/IBW"], "mL/kg"),
                ("Insp", p_data["Insp"], "s")
            ]
            top_panel(background)
            draw_right_panel_revised(background)
            bottom_panel_revised(background, parameter_data)
            bottom_panel_bar(background, onpanel=active_bottom_panel_idx)
            mid_panel_bar(background, onpanel=active_mid_panel_idx)
            if active_mid_panel_idx == 0:
                mid_panel(background, parameter_data)
                draw_waveforms_dynamic(background, 10, 145, 725, 430,
                                   Ppeak_val=float(p_data['Ppeak']),
                                   TVe_val=float(p_data['TVe']),
                                   PEEP_val=float(p_data['PEEP']),
                                   t_offset=t,
                                   freq=float(p_data['ftotal']))
            if show_vac_setup:
                draw_vac_setup_popup(background)
            cv2.imshow("Ventilator UI Final", background)
            t += (1.0 / fps) * 0.5
            if cv2.waitKey(delay) & 0xFF == 27:
                break
        except Exception as e:
            print("An error occurred in the main loop:")
            traceback.print_exc()
            break
    cv2.destroyAllWindows()
