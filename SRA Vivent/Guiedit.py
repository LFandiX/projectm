import cv2
import numpy as np
import math
import time
import struct
import datetime
import os


# ========Dummy data flow untuk grafik========
MAX_POINTS = 100          # jumlah titik di layar
flow_buffer = [0] * MAX_POINTS

start_time = time.time()

# --- VARIABEL PEREKAMAN & PLAYBACK ---
is_recording = False
recorded_data = []

selected_recording_file = None
current_playback_data = []
playback_index = 0
playback_start_time = 0
is_playing = False
playback_speed = 1.0
playback_rects = [] # Stores clickable rectangles for recordings (x, y, w, h, filename)

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

def load_recording_data(filename):
    data = []
    try:
        with open(filename, "rb") as f:
            while True:
                chunk = f.read(16)  # 8 bytes for timestamp (double), 8 bytes for value (double)
                if not chunk:
                    break
                ts, val = struct.unpack("dd", chunk)
                data.append((ts, val))
        print(f"Loaded {len(data)} samples from {filename}")
    except Exception as e:
        print(f"ERROR: Could not load recording data from {filename}. Reason: {e}")
        data = []
    return data


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

    buttons_left = ["Airway", "Breath Views", "High Pressure", "Low Pressure", "Recordings"]

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
    if active_bottom_view == "flow":
        header_title = "Airway Flow"
    elif active_bottom_view == "recordings":
        header_title = "Recordings Archive"
    else:
        header_title = "Airway / Graph"

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
    
    elif active_bottom_view == "recordings":
        draw_recordings_view(img)
    
    elif active_bottom_view == "playback":
        draw_playback_view(img)

    # 4. Konten Bar Bawah (Tombol)
    BOTTOM_BUTTONS_DEFAULT = ["Flow", "Pressure", "Volume", "Oxygen", "Cancel"]
    BOTTOM_BUTTONS_FLOW = ["Zero", "Stop", "Clear", "Autoscale On", "Save"]
    BOTTOM_BUTTONS_RECORDINGS = [] # Clean bottom bar for recordings list
    BOTTOM_BUTTONS_PLAYBACK = []   # Playback view draws its own controls

    if active_bottom_view == "flow":
        buttons_bottom = BOTTOM_BUTTONS_FLOW
    elif active_bottom_view == "recordings":
        buttons_bottom = BOTTOM_BUTTONS_RECORDINGS
    elif active_bottom_view == "playback":
        buttons_bottom = BOTTOM_BUTTONS_PLAYBACK
    else:
        buttons_bottom = BOTTOM_BUTTONS_DEFAULT

    num_btns = len(buttons_bottom)
    
    if num_btns > 0:
        btn_width = (WIDTH - LEFT_MENU_WIDTH) // num_btns

        for i, text in enumerate(buttons_bottom):
            x_start = LEFT_MENU_WIDTH + i * btn_width

            current_text = text
            
            # Override for Recording state
            if active_bottom_view == "flow" and i == 4 and is_recording:
                current_text = "SAVING..."
                # Draw red background for active recording
                cv2.rectangle(img, (x_start, HEIGHT - BOTTOM_BAR_HEIGHT), (x_start + btn_width, HEIGHT), (0, 0, 200), -1)

            # text center
            text_size = cv2.getTextSize(current_text, FONT, 0.7, 1)[0]
            text_x = x_start + (btn_width - text_size[0]) // 2
            text_y = HEIGHT - 25

            cv2.putText(img, current_text, (text_x, text_y),
                        FONT, 0.7, COLOR_TEXT_WHITE, 1)

            if i < num_btns - 1:
                cv2.line(img,
                        (x_start + btn_width, HEIGHT - BOTTOM_BAR_HEIGHT),
                        (x_start + btn_width, HEIGHT),
                        COLOR_SEPARATOR, 1)

    return img


def draw_playback_view(img):
    global current_playback_data, playback_index, is_playing, playback_start_time, selected_recording_file, playback_speed

    if not current_playback_data:
        cv2.putText(img, "No data loaded for playback.", (LEFT_MENU_WIDTH + 20, TOP_BAR_HEIGHT + 100), FONT, 0.7, COLOR_TEXT_DARK, 2)
        return

    # Header showing filename
    cv2.putText(img, f"Playing: {selected_recording_file}", (LEFT_MENU_WIDTH + 20, TOP_BAR_HEIGHT + 35), FONT, 0.7, COLOR_TEXT_DARK, 1)

    # Display current value and timestamp
    if current_playback_data and 0 <= playback_index < len(current_playback_data):
        current_ts, current_val = current_playback_data[playback_index]
        display_time = datetime.datetime.fromtimestamp(current_ts).strftime('%H:%M:%S.%f')[:-3]
        cv2.putText(img, f"Time: {display_time}  Value: {current_val:.2f}",
                    (LEFT_MENU_WIDTH + 20, TOP_BAR_HEIGHT + 75), FONT, 0.6, COLOR_TEXT_DARK, 1)

    # === GRAPH AREA ===
    gx1 = LEFT_MENU_WIDTH + 20
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

    # Y labels (assuming flow values are in range -100 to 100 based on dummy data)
    cv2.putText(img, "100", (gx1 + 5, gy1 + 15), FONT, 0.4, COLOR_TEXT_DARK, 1)
    cv2.putText(img, "0", (gx1 + 15, axis_y + 5), FONT, 0.4, COLOR_TEXT_DARK, 1)
    cv2.putText(img, "-100", (gx1 + 5, gy2 - 5), FONT, 0.4, COLOR_TEXT_DARK, 1)

    # === Render Playback Graph ===
    if current_playback_data:
        graph_points = []
        for i in range(max(0, playback_index - MAX_POINTS), playback_index):
            if i < len(current_playback_data):
                _, value = current_playback_data[i]
                x_pos = gx1 + 40 + (i - max(0, playback_index - MAX_POINTS)) * (gx2 - (gx1 + 40)) // MAX_POINTS
                y_pos = map_value_to_y(value, gy1, gy2)
                graph_points.append((x_pos, y_pos))

        for i in range(1, len(graph_points)):
            cv2.line(img, graph_points[i-1], graph_points[i], (0, 150, 0), 2) # Green playback line
    
    # === Playback Controls ===
    control_y = HEIGHT - BOTTOM_BAR_HEIGHT + 10
    control_x_start = LEFT_MENU_WIDTH + 20
    button_spacing = 100

    # Play/Pause Button
    play_pause_text = "PAUSE" if is_playing else "PLAY"
    cv2.rectangle(img, (control_x_start, control_y), (control_x_start + 80, control_y + 40), (100, 100, 100), -1)
    cv2.putText(img, play_pause_text, (control_x_start + 10, control_y + 25), FONT, 0.6, COLOR_TEXT_WHITE, 1)

    # Stop Button
    stop_x = control_x_start + button_spacing
    cv2.rectangle(img, (stop_x, control_y), (stop_x + 80, control_y + 40), (100, 100, 100), -1)
    cv2.putText(img, "STOP", (stop_x + 10, control_y + 25), FONT, 0.6, COLOR_TEXT_WHITE, 1)

    # Speed controls
    speed_x = stop_x + button_spacing
    speed_button_width = 40
    
    # Speed - button
    cv2.rectangle(img, (speed_x, control_y), (speed_x + speed_button_width, control_y + 40), (100, 100, 100), -1)
    cv2.putText(img, "-", (speed_x + 10, control_y + 25), FONT, 0.6, COLOR_TEXT_WHITE, 1)

    # Speed text display
    cv2.putText(img, f"{playback_speed:.1f}x", (speed_x + speed_button_width + 5, control_y + 25), FONT, 0.6, COLOR_TEXT_DARK, 1)

    # Speed + button
    speed_plus_x = speed_x + speed_button_width + 45
    cv2.rectangle(img, (speed_plus_x, control_y), (speed_plus_x + speed_button_width, control_y + 40), (100, 100, 100), -1)
    cv2.putText(img, "+", (speed_plus_x + 10, control_y + 25), FONT, 0.6, COLOR_TEXT_WHITE, 1)


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






def draw_recordings_view(img):
    global playback_rects
    playback_rects = [] # Clear previous rects for fresh drawing

    # Title
    cv2.putText(img, "Recorded Files (.bin) - Newest First", (LEFT_MENU_WIDTH + 20, TOP_BAR_HEIGHT + 40), FONT, 0.7, COLOR_TEXT_DARK, 2)
    
    # List files
    try:
        files = [f for f in os.listdir('.') if f.startswith('recording_') and f.endswith('.bin')]
        files.sort(key=lambda f: os.path.getmtime(f), reverse=True) # Sort by modification time
    except Exception as e:
        files = []
        cv2.putText(img, f"Error listing files: {e}", (LEFT_MENU_WIDTH + 20, TOP_BAR_HEIGHT + 80), FONT, 0.6, (0,0,255), 1)

    start_y = TOP_BAR_HEIGHT + 80
    line_height = 25
    max_items = 12 # Display more items

    if not files:
         cv2.putText(img, "No recordings found.", (LEFT_MENU_WIDTH + 20, start_y), FONT, 0.6, COLOR_TEXT_DARK, 1)
         return

    for i, f in enumerate(files[:max_items]): 
        # Get size
        try:
            size_bytes = os.path.getsize(f)
            size_str = f"{size_bytes/1024:.1f} KB"
        except:
            size_str = "? KB"
        
        text = f"{i+1}. {f}  [{size_str}]"
        
        # Calculate text bounding box for click detection
        text_size = cv2.getTextSize(text, FONT, 0.55, 1)[0]
        text_x = LEFT_MENU_WIDTH + 20
        text_y = start_y + i*line_height
        
        # Add a clickable rectangle slightly larger than the text
        rect_x1 = text_x - 5
        rect_y1 = text_y - text_size[1] - 5 
        rect_x2 = text_x + text_size[0] + 5
        rect_y2 = text_y + 5
        
        playback_rects.append((rect_x1, rect_y1, rect_x2, rect_y2, f))

        cv2.putText(img, text, (text_x, text_y), FONT, 0.55, COLOR_TEXT_DARK, 1)






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
    global active_left_index, gui_image, active_bottom_view, is_recording, recorded_data, \
           selected_recording_file, current_playback_data, playback_index, is_playing, playback_start_time, playback_rects

    if event == cv2.EVENT_LBUTTONDOWN:

        # ===== LEFT MENU =====
        if x < LEFT_MENU_WIDTH and y < HEIGHT - BOTTOM_BAR_HEIGHT:
            btn_height = (HEIGHT - BOTTOM_BAR_HEIGHT) // 5
            index = y // btn_height
            if 0 <= index < 5:
                active_left_index = index
                # Logic Switch View based on Left Menu
                if index == 4: # Recordings
                    active_bottom_view = "recordings"
                    is_playing = False # Stop any ongoing playback if switching views
                else:
                    # For other buttons, reset to default or keep current?
                    # Request implied index 4 is specifically for this.
                    # If we click others, maybe go back to default?
                    # Let's say index 0 is Airway -> Default/Flow choice
                    active_bottom_view = "default" 

        # ===== BOTTOM BUTTONS (DEFAULT / FLOW ONLY) =====
        if active_bottom_view in ["default", "flow"] and y > HEIGHT - BOTTOM_BAR_HEIGHT:
            btn_width = (WIDTH - LEFT_MENU_WIDTH) // 5
            index = (x - LEFT_MENU_WIDTH) // btn_width

            if index == 0 and active_bottom_view != "flow":
                active_bottom_view = "flow"
            elif active_bottom_view == "flow":
                if index == 4:  # Save button
                    is_recording = not is_recording
                    if is_recording:
                        recorded_data = []
                        print("Recording started... (Click 'SAVING...' to stop and save)")
                    else:
                        # Save to file
                        try:
                            filename = f"recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"
                            full_path = os.path.abspath(filename)
                            print(f"Attempting to save to: {full_path}")
                            
                            with open(full_path, "wb") as f:
                                for ts, val in recorded_data:
                                    f.write(struct.pack("dd", ts, val))
                            
                            print(f"SUCCESS: Recording saved to {full_path}")
                            print(f"Total samples: {len(recorded_data)}")
                        except Exception as e:
                            print(f"ERROR: Failed to save file. Reason: {e}")
            else:
                active_bottom_view = "default"

        # ===== RECORDINGS LIST CLICK (Phase 1) =====
        if active_bottom_view == "recordings":
            for (rx1, ry1, rx2, ry2, filename_to_load) in playback_rects:
                if rx1 <= x <= rx2 and ry1 <= y <= ry2:
                    print(f"Clicked on recording: {filename_to_load}")
                    selected_recording_file = filename_to_load
                    current_playback_data = load_recording_data(filename_to_load)
                    playback_index = 0
                    is_playing = False # Start paused
                    playback_start_time = 0 # Will be set on play
                    active_bottom_view = "playback" # Transition to playback view
                    gui_image = draw_gui() # Redraw immediately
                    return # Exit mouse_callback, as we've handled the click
        
        # ===== PLAYBACK CONTROLS CLICK =====
        elif active_bottom_view == "playback":
            control_y_start = HEIGHT - BOTTOM_BAR_HEIGHT + 10
            control_y_end = control_y_start + 40
            control_x_start = LEFT_MENU_WIDTH + 20
            button_width = 80
            button_spacing = 100

            # Play/Pause button
            play_pause_x1 = control_x_start
            play_pause_x2 = control_x_start + button_width
            if play_pause_x1 <= x <= play_pause_x2 and control_y_start <= y <= control_y_end:
                if not current_playback_data: return
                is_playing = not is_playing
                if is_playing:
                    # Sync playback start time to current real time
                    if playback_index == 0: # If starting from beginning
                        playback_start_time = time.time()
                    else: # If resuming from pause
                        # Adjust playback_start_time to account for elapsed real time vs elapsed recording time
                        recorded_time_at_pause = current_playback_data[playback_index][0] - current_playback_data[0][0]
                        playback_start_time = time.time() - recorded_time_at_pause / playback_speed
                print(f"Playback {'resumed' if is_playing else 'paused'}")
            
            # Stop button
            stop_x1 = control_x_start + button_spacing
            stop_x2 = stop_x1 + button_width
            if stop_x1 <= x <= stop_x2 and control_y_start <= y <= control_y_end:
                print("Playback stopped")
                is_playing = False
                playback_index = 0
                playback_start_time = 0
                active_bottom_view = "recordings" # Go back to recordings list
                gui_image = draw_gui() # Redraw immediately
                return # Exit mouse_callback
            
            # Speed controls
            speed_x = control_x_start + button_spacing * 2
            speed_button_width = 40

            # Speed - button
            speed_minus_x1 = speed_x
            speed_minus_x2 = speed_x + speed_button_width
            if speed_minus_x1 <= x <= speed_minus_x2 and control_y_start <= y <= control_y_end:
                playback_speed = max(0.1, playback_speed - 0.1) # Minimum speed 0.1x
                print(f"Playback speed set to {playback_speed:.1f}x")
            
            # Speed + button
            speed_plus_x1 = speed_x + speed_button_width + 45
            speed_plus_x2 = speed_x + speed_button_width + 45 + speed_button_width
            if speed_plus_x1 <= x <= speed_plus_x2 and control_y_start <= y <= control_y_end:
                playback_speed = min(4.0, playback_speed + 0.1) # Maximum speed 4.0x
                print(f"Playback speed set to {playback_speed:.1f}x")

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

        if is_recording:
            recorded_data.append((time.time(), new_value))
        
        # Playback logic
        if active_bottom_view == "playback" and is_playing and current_playback_data:
            if playback_start_time == 0: # If just started playing, set initial time
                playback_start_time = time.time()

            elapsed_time_since_play_start = (time.time() - playback_start_time) * playback_speed
            
            # Find the corresponding index in current_playback_data
            # We want to find the first sample whose relative timestamp (from start of recording)
            # is greater than or equal to elapsed_time_since_play_start
            
            initial_recorded_ts = current_playback_data[0][0] if current_playback_data else 0

            found_index = -1
            for i in range(playback_index, len(current_playback_data)): # Start search from current index to be efficient
                relative_recorded_time = (current_playback_data[i][0] - initial_recorded_ts)
                if relative_recorded_time >= elapsed_time_since_play_start:
                    found_index = i
                    break
            
            if found_index != -1 and found_index < len(current_playback_data):
                playback_index = found_index
            else:
                # Reached end of recording or no data
                playback_index = len(current_playback_data) - 1 if current_playback_data else 0
                is_playing = False
                print("Playback finished.")

        gui_image = draw_gui()

        cv2.imshow(window_name, gui_image)
        
        # Tunggu input keyboard (1ms delay)
        key = cv2.waitKey(1) & 0xFF
        
        # Jika 'q' ditekan, keluar loop
        if key == ord('q'):
            if is_recording:
                print("Exiting while recording. Saving data...")
                try:
                    filename = f"recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.bin"
                    full_path = os.path.abspath(filename)
                    with open(full_path, "wb") as f:
                        for ts, val in recorded_data:
                            f.write(struct.pack("dd", ts, val))
                    print(f"Saved to {full_path}")
                except Exception as e:
                    print(f"Error saving on exit: {e}")
            break

    cv2.destroyAllWindows()