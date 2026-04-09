import cv2
import numpy as np
import math
import random

# Ukuran window
W, H = 1280, 720
White = (255, 255, 255)

# --------------------------------
# Fungsi bantu teks di tengah box
def put_centered_text(img, text, top_left, bottom_right, font=cv2.FONT_HERSHEY_SIMPLEX,
                      font_scale=1, color=(255,255,255), thickness=2):
    (x1, y1) = top_left
    (x2, y2) = bottom_right
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    org_x = center_x - text_w // 2
    org_y = center_y + text_h // 2
    cv2.putText(img, text, (org_x, org_y), font, font_scale, color, thickness, cv2.LINE_AA)

# --------------------------------
# Panel Kiri 
def draw_left_panel(img, params):
    cv2.line(img, (300,0), (300,H), (255,255,255), 10)

    # tinggi box per param
    box_height = H // len(params)

    for i, (label, val, unit) in enumerate(params):
        y_top = i * box_height
        y_bottom = (i+1) * box_height

        # background box biru tua
        cv2.rectangle(img, (0, y_top), (300, y_bottom), (150, 50, 50), -1)

        # label kecil di atas
        cv2.putText(img, label, (10, y_top+30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)

        # value di tengah
        (tw, th), _ = cv2.getTextSize(val, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 2)
        cv2.putText(img, val, (20, y_top + box_height//2 + th//2),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2, cv2.LINE_AA)

        # unit di kanan bawah
        if unit:
            cv2.putText(img, unit, (200, y_top + box_height - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2, cv2.LINE_AA)

        # garis pemisah
        cv2.line(img, (0, y_bottom), (300, y_bottom), (255,255,255), 10)

# --------------------------------
# Panel Kanan
def draw_right_panel(img):
    cv2.line(img,(1000,0),(1000,520),White,10)
    boxes = [("Start",(1020,10),(1260,120),(0,0,0)),
             ("Stop",(1020,130),(1260,240),(200,100,0)),
             ("Modes",(1020,250),(1260,360),(0,0,0)),
             ("Alarm limits",(1020,370),(1260,480),(200,100,0))]
    for text, tl, br, fill in boxes:
        if fill != (0,0,0): cv2.rectangle(img,tl,br,fill,-1)
        cv2.rectangle(img,tl,br,White,1)
        put_centered_text(img,text,tl,br,font_scale=1,color=White)

# --------------------------------
# Panel Bawah (Lingkaran)
def draw_bottom_panel(img, values):
    cv2.line(img,(300,520),(1280,520),White,10)

    centers = [(500,600),(700,600),(900,600),(1100,600)]
    labels = ["Pin","Pexp","I:E","RR"]
    for i, (center,val,label) in enumerate(zip(centers,values,labels)):
        radius = 60
        cv2.circle(img, center, radius, (255,255,255), -1)
        cv2.circle(img, center, radius, (180,180,180), 20)
        cv2.circle(img, (center[0], center[1]-radius//2), 12, (0,0,255), -1)
        (tw,th),_ = cv2.getTextSize(val, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 3)
        cv2.putText(img,val,(center[0]-tw//2,center[1]+th//2),cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,0,0),3,cv2.LINE_AA)
        (tw,th),_ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        cv2.putText(img,label,(center[0]-tw//2,center[1]+radius+40),cv2.FONT_HERSHEY_SIMPLEX,1,White,2,cv2.LINE_AA)

# --------------------------------
# Panel Tengah (Title + Grafik)
def draw_center_panel(img, title, mode, graph_points):
    font = cv2.FONT_HERSHEY_SIMPLEX
    (tw,th),_ = cv2.getTextSize(title,font,1,2)
    cv2.putText(img,title,(650-tw//2,50),font,1,White,2,cv2.LINE_AA)
    cv2.putText(img,"Pressure",(310,130),font,0.8,White,2,cv2.LINE_AA)
    label = f"Mode: {mode}"
    (tw,th),_ = cv2.getTextSize(label,font,0.8,2)
    cv2.putText(img,label,(970-tw,130),font,0.8,White,2,cv2.LINE_AA)

    # Gambar grafik
    for i in range(len(graph_points)-1):
        cv2.line(img, graph_points[i], graph_points[i+1], (0,0,0), 4)

# --------------------------------
# Main GUI
def main_gui(params, values, graph_points):
    img = np.zeros((H,W,3),dtype=np.uint8)
    img[:] = (150,50,50)
    draw_left_panel(img, params)
    draw_right_panel(img)
    draw_bottom_panel(img, values)
    draw_center_panel(img,"Exovent Qatar","CYCLIC",graph_points)
    return img

# --------------------------------
# Grafik bergerak
graph_points = [(x,400) for x in range(330,970,10)]
t = 0
temp = 22.0
ie_modes = ["1:2","1:3","1:4"]
ie_idx = 0

while True:
    # update params dinamis
    Pin_val  = 20 + 5*math.sin(t/20)
    Pexp_val = 5 + 2*math.cos(t/25)
    RR_val   = 18 + random.randint(-2,2)
    Temp_val = temp + 0.01*math.sin(t/100)  # lambat berubah
    IE_val   = ie_modes[ie_idx//100 % len(ie_modes)]

    params = [
    ("Pin",  f"{Pin_val:.2f}",  "cmH2O"),
    ("Pexp", f"{Pexp_val:.2f}", "cmH2O"),
    ("I:E",  IE_val,            ""),       # ga ada unit
    ("RR",   f"{RR_val:.2f}",   "bpm"),
    ("Temp", f"{Temp_val:.2f}", "C")
]

    values = [f"{Pin_val:.0f}", f"{Pexp_val:.0f}", IE_val, f"{RR_val}"]

    # Geser grafik
    graph_points = [(x-5, y) for (x,y) in graph_points if x-5 > 330]
    new_x = 970
    new_y = 300 + int(100*math.sin(t/15))  # gelombang sinus
    graph_points.append((new_x,new_y))
    t += 1

    # Render GUI
    img = main_gui(params, values, graph_points)
    cv2.imshow("Ventilator GUI Dynamic Params", img)

    if cv2.waitKey(50) & 0xFF == 27:  # ESC keluar
        break

cv2.destroyAllWindows()
