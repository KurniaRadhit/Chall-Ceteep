# FORENSIC

## Author

Nikoo

## Categories

Digital Forensic

## Description

Flag format: `LKS{...}`

## Attachment

- `chall.pcapng`
  
## Solver

### Step 1: Cari path yang berhasil ditemukan saat fuzzing
Trafik HTTP didominasi ribuan request fuzzing directory yang dijawab 404. Abaikan semuanya dan saring hanya respons berstatus 200, karena itu adalah path yang benar-benar ada di server:
```bash
tshark -r chall.pcapng -Y 'http.response.code==200' \
  -T fields -e frame.number -e http.response_for.uri | head -30
```
**Hasil:** selain halaman web biasa (`/`, `index.html`, `about.html`, dan sejenisnya), muncul path yang janggal: `/.git/HEAD` dengan status 200. Folder `.git` terekspos di web server.

---

### Step 2: Identifikasi file repositori yang diunduh
Setelah menemukan `.git`, penyerang mengunduh metadata repositori lalu packfile yang berisi seluruh objek.
```bash
tshark -r chall.pcapng -Y 'http.request.uri contains ".git/"' \
  -T fields -e frame.time_relative -e http.request.uri | sort -u -k2
```
**Hasil:** selain `HEAD`, `config`, `packed-refs`, dan `objects/info/packs`, penyerang mengunduh `/.git/objects/pack/pack-87edf918cdebea2407813ba96915a7b2348b9ae8.pack` beserta `.idx`.

---

### Step 3: Ekstrak objek HTTP dari pcap
Gunakan `File → Export Objects → HTTP` di Wireshark (filter teks `pack`), atau lewat terminal:
```bash
mkdir out && tshark -r chall.pcapng --export-objects http,out -q
ls -l out/pack-87edf918*
```
Ukuran file harus utuh: `.idx` = **1772** byte dan `.pack` = **3187** byte. Folder `out` juga berisi ribuan file 153 byte (halaman 404); abaikan semuanya.

---

### Step 4: Susun ulang repositori
Buat repositori kosong, lalu letakkan packfile dan indeksnya di direktori objek Git.
```bash
mkdir rec && cd rec && git init -q
cp ../out/pack-87edf918*.pack ../out/pack-87edf918*.idx .git/objects/pack/
git verify-pack -v .git/objects/pack/pack-*.idx | tail -3
```
Baris terakhir harus berakhiran `...pack: ok` (14 objek).

---

### Step 5: Pulihkan referensi branch
Folder `refs/` tidak ikut terunduh, jadi `git log` awalnya kosong. Ada dua cara:

**Cara 1: pakai `packed-refs`** (diunduh penyerang di Step 2)
```bash
cat ../out/packed-refs
git symbolic-ref HEAD refs/heads/main
git update-ref refs/heads/main 5161cf2ce351df888176ad68fdce0a75d81c5133
git log --oneline
```

**Cara 2: tanpa `packed-refs`**
```bash
git cat-file --batch-all-objects --batch-check | grep commit
git fsck --lost-found 2>&1 | head
git log --oneline <hash-commit>
```

Riwayat yang terlihat (6 commit):
```
5161cf2 Add tracking placeholder
595e48c Housekeeping
67f65f1 Add contact page
0d21ec3 Add deployment config
4cf4184 Add about page
f1cdf43 Initial commit: landing page
```

---

### Step 6: Temukan flag di commit lama
File konfigurasi ditambahkan pada commit `0d21ec3` ("Add deployment config"), lalu dihapus pada commit `595e48c` ("Housekeeping") dan hanya dimasukkan ke `.gitignore`. Karena itu ia tidak tampak di versi terbaru, tetapi masih tersimpan di history.
```bash
git log -p -S"LKS{" | grep LKS
# atau langsung
git show 0d21ec3
```
Isi `config.env` pada commit `0d21ec3`:
```
APP_ENV=production
DB_HOST=10.0.10.15
DB_USER=arunika_app
DB_PASS=Arunika_Db_2026
INTERNAL_TOKEN=LKS{a6c4e8f2d1b90735c5a9e3f6b2d10487}
```

## Flag

`LKS{a6c4e8f2d1b90735c5a9e3f6b2d10487}`
