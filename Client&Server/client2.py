import socket
import threading

# Masukkan IP server
SERVER_IP = input("Masukkan IP server: ")
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))

# Fungsi untuk menerima pesan dari server
def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            print("🔴 Koneksi ke server terputus.")
            client.close()
            break

# Buat thread untuk menerima pesan
thread = threading.Thread(target=receive_messages)
thread.start()

# Kirim pesan ke server
while True:
    pesan = input()
    client.send(pesan.encode())
    if pesan == "/keluar":
        break

client.close()
