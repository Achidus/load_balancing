# Python Socket Load Balancing

Simulasi load balancing menggunakan Python dan TCP Socket dengan
satu broker dan tiga worker.

## Fitur
- Client-server menggunakan TCP Socket
- Broker untuk mendistribusikan request
- Tiga worker server
- Algoritma Round Robin
- Algoritma Least Requests
- Application ID SHORT dan LONG
- Komunikasi menggunakan JSON

## Teknologi
- Python 3
- Socket
- Threading
- JSON

## Cara Menjalankan

Jalankan setiap perintah di terminal terpisah.

### Worker 1
python3 worker.py 9001 Worker-1

### Worker 2
python3 worker.py 9002 Worker-2

### Worker 3
python3 worker.py 9003 Worker-3

### Broker
python3 broker.py

### Client
python3 client.py

Pastikan port broker pada broker.py dan client.py sama.
Konfigurasi saat ini menggunakan port 9100.

## Algoritma

- ROUND_ROBIN: memilih worker secara bergiliran.
- LEAST_REQUESTS: memilih worker berdasarkan jumlah request
  selesai ditambah request yang sedang diproses.

## Tujuan
Project pembelajaran jaringan komputer dan dasar cybersecurity.
