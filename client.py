
import socket
import json

HOST = "127.0.0.1"
PORT = 9100


def send_request(app_id, message, strategy):
    request = {
        "app_id": app_id.upper(),
        "message": message,
        "strategy": strategy
    }

    try:
        with socket.create_connection((HOST, PORT), timeout=35) as sock:
            sock.settimeout(35)

            sock.sendall(
                (json.dumps(request) + "\n").encode("utf-8")
            )

            with sock.makefile("r", encoding="utf-8") as file:
                response = file.readline()

            if response:
                print("\nRespons dari broker:")
                print(json.dumps(
                    json.loads(response),
                    indent=4,
                    ensure_ascii=False
                ))
            else:
                print("Broker tidak memberikan respons.")

    except (OSError, json.JSONDecodeError) as e:
        print(f"Gagal menghubungi broker: {e}")


if __name__ == "__main__":
    print("=== CLIENT LOAD BALANCING ===")

    app_id = input("Application ID (SHORT/LONG): ").strip().upper()

    if app_id not in ("SHORT", "LONG"):
        print("Application ID tidak valid. Masukkan SHORT atau LONG.")
    else:
        message = input("Pesan: ").strip()

        print("Strategi:")
        print("1. LEAST_REQUESTS")
        print("2. ROUND_ROBIN")

        pilihan = input("Pilih strategi (1/2): ").strip()

        strategy = {
            "1": "LEAST_REQUESTS",
            "2": "ROUND_ROBIN"
        }.get(pilihan)

        if strategy is None:
            print("Strategi tidak valid.")
        else:
            send_request(app_id, message, strategy)
