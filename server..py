import socket
import threading
import random

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    try:
       
        command = conn.recv(1024).decode().strip()
        print(f"[COMMAND] {command}")
        conn.sendall("Input numbers\n".encode())  # Step 2: Svar

       
        numbers = conn.recv(1024).decode().strip()
        print(f"[NUMBERS] {numbers}")
        tal1, tal2 = map(int, numbers.split())

 
        if command == "Random":
            result = random.randint(tal1, tal2)
        elif command == "Add":
            result = tal1 + tal2
        elif command == "Subtract":
            result = tal1 - tal2
        else:
            result = "Unknown command"

        conn.sendall(f"{result}\n".encode())
        print(f"[RESULT SENT] {result}")
    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")

def start_server(host="127.0.0.1", port=65431):  # Bruger en anden port end json_server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[SERVER STARTED] Listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
