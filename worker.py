
import socket
import json
import sys
import time
import threading

HOST = "127.0.0.1"
PORT = int(sys.argv[1])
WORKER_ID = sys.argv[2]

def process_request(request):
    app_id = request.get("app_id", "").upper()
    message = request.get("message", "")

    if app_id == "SHORT":
        result = f"Echo: {message}"
    elif app_id == "LONG":
        # Simulasi perhitungan lebih kompleks
        total = sum(i * i for i in range(1, 500_001))
        result = f"Perhitungan selesai: {total}"
    else:
        return {
            "status": "error",
            "worker": WORKER_ID,
            "message": "Application ID tidak dikenal"
        }

    return {
        "status": "success",
        "worker": WORKER_ID,
        "app_id": app_id,
        "result": result
    }

def handle_client(conn, addr):
    with conn:
        try:
            file = conn.makefile("r", encoding="utf-8")
            line = file.readline()
            if not line:
                return

            request = json.loads(line)
            print(f"[{WORKER_ID}] Request dari broker: {request}")

            response = process_request(request)
            print(f"[{WORKER_ID}] Hasil: {response}")

            conn.sendall(
                (json.dumps(response) + "\n").encode("utf-8")
            )
        except Exception as e:
            print(f"[{WORKER_ID}] Error: {e}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"[{WORKER_ID}] Berjalan pada {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            ).start()

if __name__ == "__main__":
    main()
