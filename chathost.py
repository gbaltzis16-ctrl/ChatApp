import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

clients = []

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    clients.append(client_socket)

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[{addr}] {data.decode().strip()}")
            for client in clients:
                if client != client_socket:
                    client.send(data)
        except:
            break

    client_socket.close()
    clients.remove(client_socket)
    print(f"[CLOSE CONNECTION] {addr} disconnected")

def start_server ():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print(f"[SERVER STARTED] {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        thread=threading.Thread(target= handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()