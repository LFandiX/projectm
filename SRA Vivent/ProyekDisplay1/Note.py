# import cv2
# def rounded_rectangle(img, top_left, bottom_right, color, radius=20, thickness=-1):
#     x1, y1 = top_left
#     x2, y2 = bottom_right

#     if thickness < 0:  # isi penuh
#         # Tengah
#         cv2.rectangle(img, (x1+radius, y1), (x2-radius, y2), color, -1)
#         cv2.rectangle(img, (x1, y1+radius), (x2, y2-radius), color, -1)

#         # Sudut bundar
#         cv2.circle(img, (x1+radius, y1+radius), radius, color, -1)
#         cv2.circle(img, (x2-radius, y1+radius), radius, color, -1)
#         cv2.circle(img, (x1+radius, y2-radius), radius, color, -1)
#         cv2.circle(img, (x2-radius, y2-radius), radius, color, -1)

#     else:  # kalau hanya garis
#         cv2.rectangle(img, (x1+radius, y1), (x2-radius, y2), color, thickness)
#         cv2.rectangle(img, (x1, y1+radius), (x2, y2-radius), color, thickness)
#         cv2.circle(img, (x1+radius, y1+radius), radius, color, thickness)
#         cv2.circle(img, (x2-radius, y1+radius), radius, color, thickness)
#         cv2.circle(img, (x1+radius, y2-radius), radius, color, thickness)
#         cv2.circle(img, (x2-radius, y2-radius), radius, color, thickness)

# # Contoh pemakaian
# # rounded_rectangle(img, (1020,10), (1260,120), (200,100,0), radius=20, thickness=-1)


# import cv2
# import numpy as np

# # Canvas background
# img = np.zeros((300, 300, 3), dtype=np.uint8)
# img[:] = (50, 50, 50)  # abu gelap

# # Posisi tengah lingkaran
# center = (150, 120)
# radius = 60

# # Lingkaran luar putih
# cv2.circle(img, center, radius, (255,255,255), 2)   # border
# cv2.circle(img, center, radius-2, (220,220,220), -1) # isi abu terang

# # Lingkaran kecil merah (indikator)
# cv2.circle(img, (center[0], center[1]-radius//2), 10, (0,0,255), -1)

# # Angka di tengah
# text = "-70"
# font = cv2.FONT_HERSHEY_SIMPLEX
# (text_w, text_h), baseline = cv2.getTextSize(text, font, 1, 2)
# cv2.putText(img, text, (center[0]-text_w//2, center[1]+text_h//2), font, 1, (0,0,0), 2, cv2.LINE_AA)

# # Label di bawah lingkaran
# label = "Pb"
# (text_w, text_h), baseline = cv2.getTextSize(label, font, 1, 2)
# cv2.putText(img, label, (center[0]-text_w//2, center[1]+radius+30), font, 1, (255,255,255), 2, cv2.LINE_AA)

# cv2.imshow("Circle GUI", img)
# cv2.waitKey(0)S
# cv2.destroyAllWindows()


# def add(a,b):
#     return a + b


import kagglehub

# Download latest version
path = kagglehub.dataset_download("PROPPG-PPG/hourly-weather-surface-brazil-southeast-region")

print("Path to dataset files:", path)







# # --- State ---
# running = False   # default berhenti

# # Koordinat tombol
# btn_start = ((1020,10),(1260,120))
# btn_stop  = ((1020,130),(1260,240))

# # Fungsi cek klik dalam area
# def inside_box(x, y, top_left, bottom_right):
#     return top_left[0] <= x <= bottom_right[0] and top_left[1] <= y <= bottom_right[1]

# def mouse_callback(event, x, y, flags, param):
#     global running
#     if event == cv2.EVENT_LBUTTONDOWN:
#         if inside_box(x,y, *btn_start):
#             running = True
#             print("Start ditekan")
#         elif inside_box(x,y, *btn_stop):
#             running = False
#             print("Stop ditekan")


# cv2.setMouseCallback("Ventilator GUI V2", mouse_callback)
    # if running:

    # else:
    #     # Jika stop → nilai tetap freeze
    #     params = [
    #         ("Pin",  "0.00"),
    #         ("Pexp", "0.00"),
    #         ("I:E",  "--"),
    #         ("RR",   "0.00"),
    #         ("Temp", f"{temp:.2f}")
    #     ]
    #     values = ["0","0","--","0"]