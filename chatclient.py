import socket
import threading

HOST = "127.0.0.1"
PORT = 5555

def listen(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(">>"+data.decode())
        except:
            break

def start_client():
    name= input("Enter your name: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    thread = threading.Thread(target=listen, args=(sock,))
    thread.start()

    print("[connected] Type messages")
    while True:
        msg = input()
        if msg.lower() == "quit":
            break
        fullmsg = f"{name}: {msg}"
        sock.send(fullmsg.encode())

    sock.close ()

if __name__ == "__main__":
    start_client()