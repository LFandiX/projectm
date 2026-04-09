import cv2
import numpy as np
import math
import random

def draw_left_panel(img, params):
    White = (255, 255, 255)
    cv2.line(img,(300,0),(300,720),White,10)

    # Pin
    cv2.putText(img,params[0][0],(10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, White, 2, cv2.LINE_AA)
    cv2.putText(img,params[0][1],(50,90), cv2.FONT_HERSHEY_SIMPLEX, 1.5, White, 2, cv2.LINE_AA)
    cv2.putText(img,'cmH2O',(170,130), cv2.FONT_HERSHEY_SIMPLEX, 1, White, 2, cv2.LINE_AA)

    # Pexp
    cv2.line(img,(0,144),(300,144),White,10)
    cv2.putText(img,params[1][0],(10,180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, White, 2, cv2.LINE_AA)
    cv2.putText(img,params[1][1],(80,235), cv2.FONT_HERSHEY_SIMPLEX, 1.5, White, 2, cv2.LINE_AA)
    cv2.putText(img,'cmH2O',(170,275), cv2.FONT_HERSHEY_SIMPLEX, 1, White, 2, cv2.LINE_AA)

    # I:E
    cv2.line(img,(0,288),(300,288),White,10)
    cv2.putText(img,params[2][0],(10,320), cv2.FONT_HERSHEY_SIMPLEX, 0.7, White, 2, cv2.LINE_AA)
    cv2.putText(img,params[2][1],(90,375), cv2.FONT_HERSHEY_SIMPLEX, 1.5, White, 2, cv2.LINE_AA)

    # RR
    cv2.line(img,(0,432),(300,432),White,10)
    cv2.putText(img,params[3][0],(10,463), cv2.FONT_HERSHEY_SIMPLEX, 0.7, White, 2, cv2.LINE_AA)
    cv2.putText(img,params[3][1],(60,515), cv2.FONT_HERSHEY_SIMPLEX, 1.5, White, 2, cv2.LINE_AA)
    cv2.putText(img,'bpm',(215,555), cv2.FONT_HERSHEY_SIMPLEX, 1, White, 2, cv2.LINE_AA)

    # Temp
    cv2.line(img,(0,576),(300,576),White,10)
    cv2.putText(img,params[4][0],(10,610), cv2.FONT_HERSHEY_SIMPLEX, 0.7, White, 2, cv2.LINE_AA)
    cv2.putText(img,params[4][1],(60,660), cv2.FONT_HERSHEY_SIMPLEX, 1.5, White, 2, cv2.LINE_AA)
    cv2.putText(img,'C',(260,710), cv2.FONT_HERSHEY_SIMPLEX, 1, White, 2, cv2.LINE_AA)

    cv2.line(img,(0,720),(300,720),White,10)

def put_centered_text(img, text, top_left, bottom_right, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(255,255,255), thickness=2):
    (x1, y1) = top_left
    (x2, y2) = bottom_right

    # Hitung ukuran teks
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)

    # Hitung posisi tengah
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    # Koordinat start teks
    org_x = center_x - text_w // 2
    org_y = center_y + text_h // 2

    cv2.putText(img, text, (org_x, org_y), font, font_scale, color, thickness, cv2.LINE_AA)

def draw_right_panel(img):
    White = (255, 255, 255)
    #Garis pembatas
    cv2.line(img,(1000,0),(1000,520),White,10)

    #Box 1
    cv2.rectangle(img,(1020,10),(1260,120),White,1)
    put_centered_text(img, "Start", (1020,10), (1260,120), font_scale=1, color=White, thickness=2)

    #Box2
    cv2.rectangle(img,(1020,130),(1260,240),(200,100,0),-1)# Warna Fill -> -1
    cv2.rectangle(img,(1020,130),(1260,240),White,1)
    put_centered_text(img, "Stop", (1020,130), (1260,240), font_scale=1, color=White, thickness=2)

    #Box3
    cv2.rectangle(img,(1020,250),(1260,360),White,1)
    put_centered_text(img, "Modes", (1020,250), (1260,360), font_scale=1, color=White, thickness=2)

    #Box4
    cv2.rectangle(img,(1020,370),(1260,480),(200,100,0),-1)# Warna Fill -> -1
    cv2.rectangle(img,(1020,370),(1260,480),White,1)
    put_centered_text(img, "Alarm limits", (1020,370), (1260,480), font_scale=1, color=White, thickness=2)

def draw_bottom_panel(img,values):
    White = (255, 255, 255)
    cv2.line(img,(300,520),(1280,520),White,10)

    # LIngkaran 1
    center = (500,600)
    radius = 60
    cv2.circle(img, center, radius, (255,255,255), -1)
    cv2.circle(img, center, radius, (180,180,180), 20)
    cv2.circle(img, (center[0], center[1]-radius//2), 12, (0,0,255), -1)

    text = values[0]
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(text, font, 0.8, 3)
    cv2.putText(img, text, (center[0]-text_w//2, center[1]+text_h//2), font, 0.8, (0,0,0), 3, cv2.LINE_AA)

    label = "Pin"
    (text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
    cv2.putText(img, label, (center[0]-text_w//2, center[1]+radius+40), font, 1, (255,255,255), 2, cv2.LINE_AA)

    # LIngkaran 2
    center = (700,600)
    radius = 60
    cv2.circle(img, center, radius, (255,255,255), -1)
    cv2.circle(img, center, radius, (180,180,180), 20)
    cv2.circle(img, (center[0], center[1]-radius//2), 12, (0,0,255), -1)

    text = values[1]
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(text, font, 0.8, 3)
    cv2.putText(img, text, (center[0]-text_w//2, center[1]+text_h//2), font, 0.8, (0,0,0), 3, cv2.LINE_AA)

    label = "Pexp"
    (text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
    cv2.putText(img, label, (center[0]-text_w//2, center[1]+radius+40), font, 1, (255,255,255), 2, cv2.LINE_AA)

    # Lingkaran 3
    center = (900,600)
    radius = 60
    cv2.circle(img, center, radius, (255,255,255), -1)
    cv2.circle(img, center, radius, (180,180,180), 20)
    cv2.circle(img, (center[0], center[1]-radius//2), 12, (0,0,255), -1)

    text = values[2]
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(text, font, 0.8, 3)
    cv2.putText(img, text, (center[0]-text_w//2, center[1]+text_h//2), font, 0.8, (0,0,0), 3, cv2.LINE_AA)

    label = "I:E"
    (text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
    cv2.putText(img, label, (center[0]-text_w//2, center[1]+radius+40), font, 1, (255,255,255), 2, cv2.LINE_AA)

    #Lingkaran 4
    center = (1100,600)
    radius = 60
    cv2.circle(img, center, radius, (255,255,255), -1)
    cv2.circle(img, center, radius, (180,180,180), 20)
    cv2.circle(img, (center[0], center[1]-radius//2), 12, (0,0,255), -1)

    text = values[3]
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(text, font, 0.8, 3)
    cv2.putText(img, text, (center[0]-text_w//2, center[1]+text_h//2), font, 0.8, (0,0,0), 3, cv2.LINE_AA)

    label = "RR"
    (text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
    cv2.putText(img, label, (center[0]-text_w//2, center[1]+radius+40), font, 1, (255,255,255), 2, cv2.LINE_AA)

def draw_center_panel(img,graph_points):
    White = (255, 255, 255)
    x_mid = (300,1000)
    y_mid = (0,520)
    label = "Exovent Qatar"
    font = cv2.FONT_HERSHEY_SIMPLEX
    (text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
    cv2.putText(img, label, (sum(x_mid)//2-text_w//2, 50), font, 1, (255,255,255), 2, cv2.LINE_AA)

    label = "Pressure"
    cv2.putText(img, label, (310, 130), font, 0.8, (255,255,255), 2, cv2.LINE_AA)

    label = "Mode: CYCLIC"
    (text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
    cv2.putText(img, label, (x_mid[1]+30-text_w, 130), font, 0.8, (255,255,255), 2, cv2.LINE_AA)

    # Remove lung capacity reference lines for pressure waveform

    #Grafik - breathing waveform
    for i in range(len(graph_points)-1):
        cv2.line(img, graph_points[i], graph_points[i+1], (0,255,0), 3)  # Green line for better visibility

def breathing_wave(t):
    # Complete breathing cycle: 240 frames (longer for smoother transitions)
    cycle = t % 240
    
    # Define lung capacity levels
    functional_residual = 350      # FRC baseline
    tidal_amplitude = 25          # Normal breathing amplitude
    inspiratory_capacity = 250    # Maximum inspiration
    expiratory_reserve = 420      # Below FRC during forced expiration
    
    if cycle < 50:
        # First normal tidal breathing cycle
        wave_progress = (cycle / 50) * 2 * math.pi
        small_wave = tidal_amplitude * math.sin(wave_progress)
        return int(functional_residual - small_wave)
    
    elif cycle < 100:
        # Second normal tidal breathing cycle
        wave_progress = ((cycle - 50) / 50) * 2 * math.pi
        small_wave = tidal_amplitude * math.sin(wave_progress)
        return int(functional_residual - small_wave)
    
    elif cycle < 140:
        # Smooth transition to deep inspiration
        progress = (cycle - 100) / 40.0
        # Start from end of small wave and smoothly rise
        start_y = functional_residual + tidal_amplitude
        target_y = inspiratory_capacity
        smooth_curve = start_y + (target_y - start_y) * (0.5 * (1 - math.cos(progress * math.pi)))
        return int(smooth_curve)
    
    elif cycle < 180:
        # Deep expiration - smooth drop to expiratory reserve
        progress = (cycle - 140) / 40.0
        start_y = inspiratory_capacity
        target_y = expiratory_reserve
        smooth_curve = start_y + (target_y - start_y) * (0.5 * (1 - math.cos(progress * math.pi)))
        return int(smooth_curve)
    
    else:
        # Smooth return to FRC baseline
        progress = (cycle - 180) / 60.0
        start_y = expiratory_reserve
        target_y = functional_residual
        smooth_return = start_y + (target_y - start_y) * (0.5 * (1 - math.cos(progress * math.pi)))
        return int(smooth_return)

def main(params, values, graph_points):
    # Ukuran window
    W, H = 1280, 720
    # Background biru polos
    img = np.zeros((H, W, 3), dtype=np.uint8)
    img[:] = (150, 50, 50)  # BGR
    draw_left_panel(img, params)
    draw_right_panel(img)
    draw_bottom_panel(img, values)
    draw_center_panel(img,graph_points)
    return img

# Main execution
graph_points = [(x,400) for x in range(330,970,10)]
t = 0
temp = 22.0
ie_modes = ["1:2","1:3","1:4"]
ie_idx = 0
cv2.namedWindow("Ventilator GUI V2")

while True:
    # update params dinamis
    Pin_val  = 20 + 5*math.sin(t/20)
    Pexp_val = 5 + 2*math.cos(t/25)
    RR_val   = 18 + random.randint(-2,2)
    Temp_val = temp + 0.01*math.sin(t/100)  # lambat berubah
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
    new_y = breathing_wave(t)  # realistic breathing wave
    graph_points.append((new_x,new_y))
    t += 1
    ie_idx += 1

    # Render GUI
    img = main(params, values, graph_points)
    cv2.imshow("Ventilator GUI V2", img)

    if cv2.waitKey(50) & 0xFF == 27:  # ESC keluar
        break

cv2.destroyAllWindows()