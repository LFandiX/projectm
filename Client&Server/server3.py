

import socket
import threading

HOST = "0.0.0.0"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()

clients = {}        # client_socket -> username
usernames = {}      # username -> client_socket
addresses = {}      # client_socket -> address

print(f"Server berjalan di {HOST}:{PORT}")

def broadcast(message, sender=None, include_sender=False):
    # print(f"📩 SERVER LOG: {message}")
    disconnected = []
    for client in clients:
        if client != sender or include_sender:
            try:
                client.send(message.encode())
            except:
                disconnected.append(client)
    
    # Baru remove client setelah selesai loop
    for client in disconnected:
        remove_client(client, silent=True)

def send_private(username, message, sender):
    if username in usernames:
        try:
            target = usernames[username]
            target.send(message.encode())
            return True
        except:
            remove_client(target)
    else:
        sender.send(f"❌ Username '{username}' tidak ditemukan.".encode())
    return False

def handle_client(client, address):
    default_name = f"User{len(clients)+1}"
    clients[client] = default_name
    usernames[default_name] = client
    addresses[client] = address

    print(f"✅ Koneksi baru dari {address}")
    client.send(f"Selamat datang! Nama sementara Anda adalah {default_name}. Gunakan '/nama [namamu]' untuk mengganti.\nKetik /info untuk melihat fitur yang tersedia.".encode())
    client.send(f'''

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>LAN Web Server</title>
</head>
<body>
  <h1>Welcome to My LAN Web Page</h1>
  <p id="greeting">Click the button to get greeted!</p>
  <button onclick="sayHello()">Say Hello</button>

  <script src="script.js"></script>
</body>
</html>


'''.encode())

#     while True:
#         try:
#             msg = client.recv(1024).decode()
#             if not msg:
#                 break

#             sender_name = clients[client]
#             print(f"📨 [{sender_name} | {address}] {msg}")

#             if msg.startswith("/nama"):
#                 parts = msg.split(" ", 1)
#                 if len(parts) < 2:
#                     client.send("⚠️ Format: /nama [namabaru]".encode())
#                     continue

#                 new_name = parts[1].strip()
#                 if new_name in usernames:
#                     client.send("⚠️ Nama sudah digunakan.".encode())
#                 else:
#                     old = clients[client]
#                     usernames.pop(old, None)
#                     clients[client] = new_name
#                     usernames[new_name] = client
#                     broadcast(f"🔁 {old} sekarang dikenal sebagai {new_name}")
#             elif msg.startswith("to "):
#                 parts = msg.split(" ", 2)
#                 if len(parts) < 3:
#                     client.send("⚠️ Format: to [username] [pesan]".encode())
#                 else:
#                     target, pesan = parts[1], parts[2]
#                     send_private(target, f"🔵 [Private dari {sender_name}]: {pesan}", client)
#             elif msg.strip() == "/list":
#                 online_users = ", ".join(clients.values())
#                 client.send(f"🟢 Pengguna online: {online_users}".encode())
#             elif msg.strip() == "/info":
#                 fitur = (
#                     "📘 Fitur Tersedia:\n"
#                     "/nama [namabaru] - Ganti nama Anda\n"
#                     "to [username] [pesan] - Kirim pesan privat\n"
#                     "/list - Lihat siapa saja yang online\n"
#                     "/info - Lihat daftar perintah"
#                 )
#                 client.send(fitur.encode())
#             else:
#                 broadcast(f"💬 {sender_name}: {msg}", sender=client)
#         except:
#             break

#     remove_client(client)

def remove_client(client, silent=False):
    if client in clients:
        name = clients[client]
        usernames.pop(name, None)
        clients.pop(client, None)
        addresses.pop(client, None)

        try:
            client.close()
        except:
            pass

        if not silent:
            print(f"❌ {name} telah keluar.")
            broadcast(f"❌ {name} telah keluar.")

# Main loop
try:
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_client, args=(client, addr), daemon=True).start()
except KeyboardInterrupt:
    print("\n🔒 Server dimatikan.")
    server.close()



