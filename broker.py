
import socket
import json
import threading

HOST = "127.0.0.1"
BROKER_PORT = 9100

WORKERS = [
    ("Worker-1", "127.0.0.1", 9001),
    ("Worker-2", "127.0.0.1", 9002),
    ("Worker-3", "127.0.0.1", 9003),
]

# Jumlah request yang sudah selesai dilayani masing-masing worker
request_count = {worker[0]: 0 for worker in WORKERS}

# Jumlah request yang sedang diproses masing-masing worker
active_count = {worker[0]: 0 for worker in WORKERS}

# Counter untuk strategi Round Robin
round_robin_counter = 0

lock = threading.Lock()


def select_worker(strategy):
    global round_robin_counter

    with lock:
        if strategy == "ROUND_ROBIN":
            worker = WORKERS[
                round_robin_counter % len(WORKERS)
            ]
            round_robin_counter += 1

        elif strategy == "LEAST_REQUESTS":
            worker = min(
                WORKERS,
                key=lambda w: (
                    request_count[w[0]] + active_count[w[0]],
                    WORKERS.index(w)
                )
            )

        else:
            raise ValueError("Strategi load balancing tidak valid")

        active_count[worker[0]] += 1

    return worker


def forward_to_worker(worker, request):
    name, host, port = worker

    try:
        with socket.create_connection(
            (host, port), timeout=30
        ) as sock:
            sock.settimeout(30)

            with sock.makefile("r", encoding="utf-8") as file:
                sock.sendall(
                    (json.dumps(request) + "\n").encode("utf-8")
                )
                response_line = file.readline()

                if not response_line:
                    raise RuntimeError("Worker tidak memberikan respons")

                return json.loads(response_line)

    finally:
        with lock:
            active_count[name] -= 1
            request_count[name] += 1


def handle_client(conn, addr):
    with conn:
        try:
            file = conn.makefile("r", encoding="utf-8")
            line = file.readline()

            if not line:
                return

            request = json.loads(line)
            app_id = request.get("app_id", "").upper()
            strategy = request.get(
                "strategy", "ROUND_ROBIN"
            ).upper()

            if app_id not in ("SHORT", "LONG"):
                raise ValueError("Application ID harus SHORT atau LONG")

            request["app_id"] = app_id

            print(f"\n[BROKER] Request dari {addr}: {request}")

            worker = select_worker(strategy)
            print(
                f"[BROKER] Strategi={strategy}, "
                f"worker terpilih={worker[0]}"
            )

            response = forward_to_worker(worker, request)

            print(f"[BROKER] Respons dari {worker[0]}: {response}")

            conn.sendall(
                (json.dumps(response) + "\n").encode("utf-8")
            )

        except Exception as e:
            error = {"status": "error", "message": str(e)}
            print(f"[BROKER] Error: {e}")

            try:
                conn.sendall(
                    (json.dumps(error) + "\n").encode("utf-8")
                )
            except OSError:
                pass


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, BROKER_PORT))
        server.listen()

        print(f"[BROKER] Berjalan pada {HOST}:{BROKER_PORT}")

        while True:
            conn, addr = server.accept()
            threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            ).start()


if __name__ == "__main__":
    main()
