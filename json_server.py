import socket
import threading
import json
import random

def handle_client(conn, addr):
    print(f"[CONNECTED] {addr}")
    try:
        data = conn.recv(1024).decode().strip()
        print(f"[RECEIVED] {data}")

        try:
            request = json.loads(data)
        except json.JSONDecodeError:
            conn.sendall(json.dumps({"result": "Error: invalid JSON"}).encode())
            print(f"[ERROR] Invalid JSON from {addr}")
            return

        method = request.get("method")
        tal1 = request.get("Tal1")
        tal2 = request.get("Tal2")

        if method == "Random":
            result = random.randint(tal1, tal2)
        elif method == "Add":
            result = tal1 + tal2
        elif method == "Subtract":
            result = tal1 - tal2
        else:
            result = "Unknown method"

        response = json.dumps({"result": result})
        conn.sendall(response.encode())
        print(f"[SENT] {response}")

    finally:
        conn.close()
        print(f"[DISCONNECTED] {addr}")

def start_json_server(host="127.0.0.1", port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[JSON SERVER STARTED] Listening on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

# <--- Dette er vigtigt
if __name__ == "__main__":
    start_json_server()
