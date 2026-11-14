#!/bin/bash
set -e

echo "[*] Build & jalankan container..."
docker compose up --build -d

echo "[*] Nunggu container siap..."
sleep 2

echo "[*] Salin binary dari container ke folder ini..."
docker cp fmt2win:/chall/chall ./chall
chmod 755 ./chall

echo "[+] Selesai. Binary ada di: $(pwd)/chall"
ls -la ./chall
