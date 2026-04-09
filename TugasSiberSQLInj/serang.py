import requests
import time

url = "http://localhost:5000/"

print("Memulai Serangan Brute Force...")
for i in range(100): # Kirim 100 percobaan login
    try:
        # Kirim username/password asal-asalan
        requests.get(url, params={'username': f'hacker{i}', 'password': '123'})
        print(f"Serangan ke-{i+1} terkirim.")
    except:
        pass
    # time.sleep(0.1) # Kalau mau agak pelan, hilangkan pagar

print("Serangan Selesai.")