import socket
import time

target_ip = "192.168.148.128" # IP AlienVault Anda
port = 22

print(f"Menyerang SSH {target_ip}...")

for i in range(50):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((target_ip, port))
        s.send(b"SSH-2.0-OpenSSH_7.2\r\n") # Pura-pura connect
        s.close()
        print(f"Ketukan ke-{i} sent.")
        time.sleep(0.2) 
    except Exception as e:
        print(e)