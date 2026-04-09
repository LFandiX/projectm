import cv2
import numpy as np
import math
import random

# --- State ---
running = False   # default berhenti

# Koordinat tombol
btn_start = ((1020,10),(1260,120))
btn_stop  = ((1020,130),(1260,240))

# Fungsi cek klik dalam area
def inside_box(x, y, top_left, bottom_right):
    return top_left[0] <= x <= bottom_right[0] and top_left[1] <= y <= bottom_right[1]

def mouse_callback(event, x, y, flags, param):
    global running
    if event == cv2.EVENT_LBUTTONDOWN:
        if inside_box(x,y, *btn_start):
            running = True
            print("Start ditekan")
        elif inside_box(x,y, *btn_stop):
            running = False
            print("Stop ditekan")

def put_centered_text(img, text, top_left, bottom_right, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255,255,255), thickness=2):
    (x1, y1) = top_left
    (x2, y2) = bottom_right
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    org_x = center_x - text_w // 2
    org_y = center_y + text_h // 2
    cv2.putText(img, text, (org_x, org_y), font, font_scale, color, thickness, cv2.LINE_AA)

def draw_right_panel(img):
    White = (255, 255, 255)
    #Garis pembatas
    cv2.line(img,(1000,0),(1000,520),White,10)

    #Box Start
    cv2.rectangle(img,btn_start[0],btn_start[1],White,2)
    put_centered_text(img, "Start", btn_start[0], btn_start[1], font_scale=1, color=White, thickness=2)

    #Box Stop
    cv2.rectangle(img,btn_stop[0],btn_stop[1],White,2)
    put_centered_text(img, "Stop", btn_stop[0], btn_stop[1], font_scale=1, color=White, thickness=2)

    #Box lain (tetap)
    cv2.rectangle(img,(1020,250),(1260,360),White,1)
    put_centered_text(img, "Modes", (1020,250), (1260,360), font_scale=1, color=White, thickness=2)

    cv2.rectangle(img,(1020,370),(1260,480),(200,100,0),-1)
    cv2.rectangle(img,(1020,370),(1260,480),White,1)
    put_centered_text(img, "Alarm limits", (1020,370), (1260,480), font_scale=1, color=White, thickness=2)


# =========================
# Panel lain tetap sama
# =========================
def draw_left_panel(img, params):
    White = (255, 255, 255)
    cv2.line(img,(300,0),(300,720),White,10)
    cv2.putText(img,params[0][0],(10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, White, 2, cv2.LINE_AA)
    cv2.putText(img,params[0][1],(50,90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, White, 2, cv2.LINE_AA)
    cv2.putText(img,'cmH2O',(170,130), cv2.FONT_HERSHEY_SIMPLEX, 1, White, 2, cv2.LINE_AA)
    # ... (bagian lain dibiarkan sama persis seperti kode kamu)

def draw_bottom_panel(img, values):
    # (isi sama seperti kode kamu)
    pass

def draw_center_panel(img,graph_points):
    White = (255, 255, 255)
    x_mid = (300,1000)
    label = "Exovent Qatar"
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
    cv2.putText(img, label, (sum(x_mid)//2-text_w//2, 50), font, 1, (255,255,255), 2, cv2.LINE_AA)

    #Grafik
    for i in range(len(graph_points)-1):
        cv2.line(img, graph_points[i], graph_points[i+1], (0,0,0), 4)

def main(params, values, graph_points):
    W, H = 1280, 720
    img = np.zeros((H, W, 3), dtype=np.uint8)
    img[:] = (150, 50, 50)
    draw_left_panel(img, params)
    draw_right_panel(img)
    draw_bottom_panel(img, values)
    draw_center_panel(img, graph_points)
    return img


# =========================
# MAIN LOOP
# =========================
graph_points = [(x,400) for x in range(330,970,10)]
t = 0
temp = 22.0
ie_modes = ["1:2","1:3","1:4"]
ie_idx = 0

cv2.namedWindow("Ventilator GUI V2")
cv2.setMouseCallback("Ventilator GUI V2", mouse_callback)

while True:
    if running:
        # update params dinamis
        Pin_val  = 20 + 5*math.sin(t/20)
        Pexp_val = 5 + 2*math.cos(t/25)
        RR_val   = 18 + random.randint(-2,2)
        Temp_val = temp + 0.01*math.sin(t/100)
        IE_val   = ie_modes[ie_idx//100 % len(ie_modes)]

        params = [
            ("Pin",  f"{Pin_val:.2f}"),
            ("Pexp", f"{Pexp_val:.2f}"),
            ("I:E",  IE_val),
            ("RR",   f"{RR_val:.2f}"),
            ("Temp", f"{Temp_val:.2f}")
        ]
        values = [f"{Pin_val:.0f}", f"{Pexp_val:.0f}", IE_val, f"{RR_val}"]

        # Geser grafik
        graph_points = [(x-5, y) for (x,y) in graph_points if x-5 > 330]
        new_x = 970
        new_y = 300 + int(100*math.sin(t/15))
        graph_points.append((new_x,new_y))
        t += 1
    else:
        # Jika stop → nilai tetap freeze
        params = [
            ("Pin",  "0.00"),
            ("Pexp", "0.00"),
            ("I:E",  "--"),
            ("RR",   "0.00"),
            ("Temp", f"{temp:.2f}")
        ]
        values = ["0","0","--","0"]

    img = main(params, values, graph_points)
    cv2.imshow("Ventilator GUI V2", img)

    if cv2.waitKey(50) & 0xFF == 27:  # ESC keluar
        break

cv2.destroyAllWindows()
