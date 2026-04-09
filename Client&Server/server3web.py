import socket
import threading
import mysql.connector

HOST = '0.0.0.0'  # Agar bisa diakses dari browser lain di jaringan lokal
PORT = 12345    # Port yang digunakan server


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="FNDDatabase.1", #Ganti Password
        database="Mahasiswa"
    )

def handle_client(client_socket):
    request = client_socket.recv(1024).decode()
    
    print(f"[REQUEST]\n{request}")
    

    try:
        with open("LabAJAX.html", "r") as f:
            content = f.read()
        
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(content)}\r\n"
            "Connection: close\r\n"
            "\r\n" +
            content
        )
    except FileNotFoundError:
        response = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            "Connection: close\r\n"
            "\r\n"
            "<h1>404 - File Not Found</h1>"
        )

    client_socket.sendall(response.encode())
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[LISTENING] Server berjalan di http://{HOST}:{PORT}")

    while True:
        client_sock, addr = server.accept()
        print(f"[CONNECTED] {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_sock,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
