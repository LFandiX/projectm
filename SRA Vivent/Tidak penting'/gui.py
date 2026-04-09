# Creating a ventilator-style GUI image using OpenCV and displaying it in Jupyter.
# The generated image will be saved to /mnt/data/ventilator_gui.png
# This code is intended to mimic the provided reference image layout using pure OpenCV drawing functions.

import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

W, H = 1000, 520
bg_color = (30, 65, 140)  # bluish background (BGR)
img = np.full((H, W, 3), bg_color, dtype=np.uint8)

# helper for text (cv2 uses BGR)
def put(text, org, scale=0.9, color=(255,255,255), thickness=2, align='lt', font=cv2.FONT_HERSHEY_SIMPLEX):
    x, y = org
    if align == 'ct':
        (w,h),_ = cv2.getTextSize(text, font, scale, thickness)
        x = int(x - w/2)
    cv2.putText(img, text, (int(x), int(y)), font, scale, color, thickness, lineType=cv2.LINE_AA)

# Header
cv2.rectangle(img, (0,0), (W,70), (12,33,94), -1)
put("Exovent Qatar", (20,45), scale=1.2, color=(220,220,255), thickness=2)
# Mode badge
cv2.rectangle(img, (W-220, 10), (W-10, 60), (20,120,200), -1)
put("Mode : CYCLIC", (W-210, 40), scale=0.7, color=(10,10,10), thickness=2)

# Left metrics panel (stacked boxes)
panel_w = 260
x0 = 10
y0 = 85
gap = 12
box_h = 80
metrics = [
    ("Pin", "19.66", "cmH2O"),
    ("Pexp", "4.54", "cmH2O"),
    ("I:E", "1:3", ""),
    ("RR", "20.00", "rpm"),
    ("Temp", "22", "°C"),
]
for i,(title,val,unit) in enumerate(metrics):
    top = y0 + i*(box_h+gap)
    cv2.rectangle(img, (x0, top), (x0+panel_w, top+box_h), (18,110,185), -1)
    # inner darker strip
    cv2.rectangle(img, (x0+6, top+6), (x0+panel_w-6, top+box_h-6), (10,70,140), -1)
    put(title, (x0+18, top+28), scale=0.7, color=(200,220,255), thickness=1)
    put(val, (x0+18, top+60), scale=1.6, color=(255,255,255), thickness=2)
    if unit:
        put(unit, (x0+120, top+60), scale=0.8, color=(200,220,255), thickness=1)

# Main waveform area (center)
wave_x = x0 + panel_w + 20
wave_y = 85
wave_w = 600
wave_h = 300
cv2.rectangle(img, (wave_x, wave_y), (wave_x+wave_w, wave_y+wave_h), (8,35,90), -1)
# inner panel
cv2.rectangle(img, (wave_x+6, wave_y+6), (wave_x+wave_w-6, wave_y+wave_h-6), (18,70,140), -1)

# draw sample waveform (sinus-like breathing curve)
num_pts = 400
xs = np.linspace(wave_x+20, wave_x+wave_w-20, num_pts)
amplitude = 80
phase = 0.7
ys = (wave_y + wave_h//2 - 30) - (np.sin(np.linspace(0, 4*np.pi, num_pts) + phase) * (amplitude * (np.exp(-((xs-(wave_x+wave_w*0.2))/(wave_w*0.6))**2))))
pts = np.vstack([xs, ys]).astype(np.int32).T
cv2.polylines(img, [pts], False, (180,230,255), 3, lineType=cv2.LINE_AA)

# draw grid lines in waveform
for i in range(1,6):
    yy = int(wave_y + i*(wave_h/6))
    cv2.line(img, (wave_x+10, yy), (wave_x+wave_w-10, yy), (10,40,90), 1, cv2.LINE_AA)

# bottom knobs (4 circular dials)
knob_centers = [
    (wave_x + 90, wave_y + wave_h + 70),
    (wave_x + 250, wave_y + wave_h + 70),
    (wave_x + 410, wave_y + wave_h + 70),
    (wave_x + 570, wave_y + wave_h + 70),
]
for idx, (cx,cy) in enumerate(knob_centers):
    cv2.circle(img, (cx,cy), 48, (50,50,50), -1)
    cv2.circle(img, (cx,cy), 44, (200,200,200), -1)
    # small red indicator dot relative to angle
    angle = -45 + idx*30
    rad = np.deg2rad(angle)
    dx = int(np.cos(rad)*28)
    dy = int(np.sin(rad)*28)
    cv2.circle(img, (cx+dx, cy+dy), 8, (0,0,200), -1)
    # label under knob
    labels = ["Pin", "Pexp", "I:E", "RR"]
    put(labels[idx], (cx, cy+78), scale=0.6, color=(240,240,240), thickness=1, align='ct')

# Right side vertical buttons
btn_w = 140
btn_x1 = W - btn_w - 10
btn_top = 90
btn_h = 78
btn_gap = 14
btns = ["Stop", "Modes", "Alarms limits"]
for i,b in enumerate(btns):
    top = btn_top + i*(btn_h+btn_gap)
    cv2.rectangle(img, (btn_x1, top), (btn_x1+btn_w, top+btn_h), (80,150,210), -1)
    cv2.rectangle(img, (btn_x1+6, top+6), (btn_x1+btn_w-6, top+btn_h-6), (18,30,70), -1)
    put(b, (btn_x1+btn_w//2, top + btn_h//2 + 8), scale=0.7, color=(220,220,255), thickness=2, align='ct')

# Rightmost vertical tiny buttons (icons)
small_btn_w = 60
small_x = W - small_btn_w - 10
small_top = btn_top + 3*(btn_h+btn_gap) + 10
for i in range(3):
    top = small_top + i*(44+10)
    cv2.rectangle(img, (small_x, top), (small_x+small_btn_w, top+44), (15,80,150), -1)
    put("🔔" if i==0 else ("🧭" if i==1 else "⚙"), (small_x+small_btn_w//2, top+30), scale=0.8, color=(255,255,255), thickness=1, align='ct')

# Add some small readouts near top-left of waveform (like numbers)
put("Ppeak", (wave_x+10, wave_y+26), scale=0.6, color=(200,220,255), thickness=1)
put("19.66", (wave_x+10, wave_y+56), scale=1.0, color=(255,255,255), thickness=2)

# Footer status bar
cv2.rectangle(img, (0, H-40), (W, H), (10,30,70), -1)
put("Status: Running    |    Patient: Adult    |    Alarm: None", (18, H-14), scale=0.6, color=(200,220,255), thickness=1)

# Save
out_path = "/mnt/data/ventilator_gui.png"
cv2.imwrite(out_path, img)

# Display inline using matplotlib (convert BGR->RGB)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(14,7))
plt.imshow(img_rgb)
plt.axis('off')
plt.title("Generated Ventilator-style GUI (OpenCV)")
plt.show()

out_path

