import cv2
import numpy as np


# Ukuran window
W, H = 1280, 720

White = (255, 255, 255)
# Background biru polos
img = np.zeros((H, W, 3), dtype=np.uint8)
img[:] = (150, 50, 50)  # BGR



# Layout Bagian Kiri
# --------------------
params = [
    ("Pin", "19.66"),
    ("Pexp", "4.54"),
    ("I:E", "1:3"),
    ("RR", "20.00"),
    ("Temp", "22")
]

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
cv2.putText(img,params[3][0],(10,610), cv2.FONT_HERSHEY_SIMPLEX, 0.7, White, 2, cv2.LINE_AA)
cv2.putText(img,params[3][1],(60,660), cv2.FONT_HERSHEY_SIMPLEX, 1.5, White, 2, cv2.LINE_AA)
cv2.putText(img,'C',(260,710), cv2.FONT_HERSHEY_SIMPLEX, 1, White, 2, cv2.LINE_AA)

cv2.line(img,(0,720),(300,720),White,10)



# Layout Bagian Kanan
# --------------------
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

# Layout Bagian Bawah
# --------------------
cv2.line(img,(300,520),(1280,520),White,10)

# LIngkaran 1
# Posisi tengah lingkaran besar
center = (500,600)
radius = 60
# Lingkaran besar isi putih
cv2.circle(img, center, radius, (255,255,255), -1)
# Border abu
cv2.circle(img, center, radius, (180,180,180), 20)
# Lingkaran kecil merah di atas
cv2.circle(img, (center[0], center[1]-radius//2), 12, (0,0,255), -1)

# Teks di tengah (angka)
text = "20"
font = cv2.FONT_HERSHEY_SIMPLEX
(text_w, text_h), baseline = cv2.getTextSize(text, font, 0.8, 3)
cv2.putText(img, text, (center[0]-text_w//2, center[1]+text_h//2), font, 0.8, (0,0,0), 3, cv2.LINE_AA)

# Label di bawah lingkaran
label = "Pin"
(text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
cv2.putText(img, label, (center[0]-text_w//2, center[1]+radius+40), font, 1, (255,255,255), 2, cv2.LINE_AA)


# LIngkaran 2
center = (700,600)
radius = 60
cv2.circle(img, center, radius, (255,255,255), -1)
cv2.circle(img, center, radius, (180,180,180), 20)
cv2.circle(img, (center[0], center[1]-radius//2), 12, (0,0,255), -1)

text = "5"
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

text = "1:3"
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

text = "20"
font = cv2.FONT_HERSHEY_SIMPLEX
(text_w, text_h), baseline = cv2.getTextSize(text, font, 0.8, 3)
cv2.putText(img, text, (center[0]-text_w//2, center[1]+text_h//2), font, 0.8, (0,0,0), 3, cv2.LINE_AA)

label = "RR"
(text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
cv2.putText(img, label, (center[0]-text_w//2, center[1]+radius+40), font, 1, (255,255,255), 2, cv2.LINE_AA)

# Tampilan Tengah
# ------------------------------
# X: 300 - 1000
# Y: 0 - 520
x_mid = (300,1000)
y_mid = (0,520)
label = "Exovent Qatar"
(text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
cv2.putText(img, label, (sum(x_mid)//2-text_w//2, 50), font, 1, (255,255,255), 2, cv2.LINE_AA)

label = "Pressure"
cv2.putText(img, label, (310, 130), font, 0.8, (255,255,255), 2, cv2.LINE_AA)

label = "Mode: CYCLIC"
(text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
cv2.putText(img, label, (x_mid[1]+30-text_w, 130), font, 0.8, (255,255,255), 2, cv2.LINE_AA)

#Grafik
cv2.line(img,(330,400),(500,400),(0,0,0),4)
cv2.line(img,(500,400),(530,200),(0,0,0),4)
cv2.line(img,(530,200),(560,400),(0,0,0),4)
cv2.line(img,(560,400),(700,400),(0,0,0),4)
cv2.line(img,(700,400),(730,200),(0,0,0),4)
cv2.line(img,(730,200),(760,400),(0,0,0),4)
cv2.line(img,(760,400),(970,400),(0,0,0),4)


# Tampilkan GUI
# ------------------------------
cv2.imshow("Ventilator GUI Static", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
