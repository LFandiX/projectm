from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time

# === KONFIGURASI ===
form_url = "https://forms.office.com/r/uJ8z54zNWq"
kelas_list = [
    "Andi-Terlambat bangun",
    "Budi-Ketinggalan bus",
    "Citra-Sakit perut",
    "Dewi-Hujan deras",
    "Eka-Kendala transportasi",
    "Fajar-Tidur larut malam",
    "Gita-Kunci rumah hilang",
    "Hendra-Terjebak macet",
    "Intan-Menunggu orang tua",
    "Joko-Ban motor bocor",
    "Kiki-Tidak mendengar alarm",
    "Lina-Menunggu adik",
    "Mira-Tugas rumah terlambat selesai",
    "Nanda-Mobil mogok",
    "Oscar-Lupa jadwal masuk",
    "Putri-Terjebak banjir",
    "Rudi-Masalah kesehatan",
    "Sinta-Terbangun kesiangan"
]

# === START BROWSER ===
service = Service(r"C:\Users\Alfandi\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(form_url)
time.sleep(10)

# === PILIH DEPARTEMEN (Junior School) ===
junior_radio_label = driver.find_element(By.XPATH, "//label[.//input[@value='Junior School']]")
junior_radio_label.click()
time.sleep(1)

# Klik Next
next_button = driver.find_element(By.XPATH, "//button[contains(., 'Next')]")
next_button.click()
time.sleep(3)

# === ISI SEMUA 18 KELAS ===
inputs = driver.find_elements(By.XPATH, "//input[@type='text']")
for i, input_box in enumerate(inputs):
    if i < len(kelas_list):
        input_box.send_keys(kelas_list[i])
        time.sleep(0.5)

# Submit form
submit_button = driver.find_element(By.XPATH, "//button[contains(., 'Submit')]")
submit_button.click()
time.sleep(2)

print("✅ Form berhasil diisi otomatis!")
driver.quit()
# === END OF CODE ===