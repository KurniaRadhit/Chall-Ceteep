# REVERSE ENGINEERING

## Author

Nikoo

## Categories

Reverse Engineering

## Description

Flag format: `LKS{...}`

## Attachment

- `Arena404.exe`

## Solver

### Step 1: Identifikasi executable

Challenge memberikan file `Arena404.exe` berupa executable Windows. Saat dijalankan, file tersebut menampilkan game pertarungan **ARENA 404**. Walaupun terlihat seperti aplikasi native, executable ini dibuat menggunakan **PyInstaller**, yang menggabungkan bootloader native dengan bytecode Python di dalam satu file.

Karena itu, kita tidak perlu memahami seluruh assembly program. Kita dapat mengekstrak modul Python yang tertanam terlebih dahulu untuk mencari logika pengolahan hadiah.

---

### Step 2: Ekstrak file EXE menggunakan pyinstxtractor

Gunakan [`pyinstxtractor`](https://github.com/extremecoders-re/pyinstxtractor) untuk membongkar arsip PyInstaller. Letakkan `pyinstxtractor.py` dan `Arena404.exe` pada direktori yang sama, kemudian jalankan:

```bash
py -3.10 pyinstxtractor.py Arena404.exe
```

Gunakan Python **3.10** karena executable challenge ini dibangun dengan versi tersebut. Versi Python yang berbeda dapat menyebabkan arsip `PYZ` tidak ikut diekstrak.

Potongan output:

```text
[+] Processing Arena404.exe
[+] Pyinstaller version: 2.1+
[+] Python version: 3.10
[+] Found 1111 files in CArchive
[+] Possible entry point: main.pyc
[+] Found 265 files in PYZ archive
[+] Successfully extracted pyinstaller archive: Arena404.exe
```

**Hasil:** terbentuk direktori `Arena404.exe_extracted` berisi file-file hasil ekstraksi, termasuk bytecode Python (`.pyc`). Pada tahap ini, file baru **diekstrak**, belum didekompilasi menjadi source Python.

---

### Step 3: Temukan modul relic.pyc

Periksa hasil ekstraksi dan cari modul `relic.pyc`, misalnya di Git Bash:

```bash
find Arena404.exe_extracted -iname '*relic*'
```

File yang dicari berada di:

```text
Arena404.exe_extracted/
└── PYZ-00.pyz_extracted/
    └── relic.pyc
```

**Hasil:** `relic.pyc` merupakan bytecode modul yang menangani hadiah setelah pertarungan. File ini menjadi fokus analisis berikutnya.

---

### Step 4: Decompile relic.pyc menggunakan PyLingual

Buka **[PyLingual](https://pylingual.io/)**, unggah file `relic.pyc` dari folder hasil ekstraksi, kemudian lihat hasil dekompilasinya. PyLingual membantu mengubah bytecode `.pyc` menjadi kode Python yang lebih mudah dibaca.

Bagian penting dari kode hasil dekompilasi adalah:

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

_KEY_PIECES = (b'ARE', b'NA404', b'-KEY', b'-26!')
_TROPHY_HEX = 'd1622e13b67557b28acf0976e608c4e33eb62a3b9bd9e3fdd58d7d017b081b329039f50a453b4d970eb65be908bc2dbf'

def reveal_trophy() -> str:
    key = b''.join(_KEY_PIECES)
    ciphertext = bytes.fromhex(_TROPHY_HEX)
    decryptor = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = PKCS7(128).unpadder()
    return (unpadder.update(padded) + unpadder.finalize()).decode('ascii')
```

Terlihat bahwa `_KEY_PIECES` adalah potongan kunci, sedangkan `_TROPHY_HEX` berisi ciphertext dalam format hexadecimal. Fungsi `reveal_trophy()` menyatukan kunci dan mendekripsi ciphertext tersebut.

**Hasil:** algoritma yang digunakan adalah **AES-128 mode ECB** dengan padding **PKCS7**. Informasi yang dibutuhkan untuk dekripsi sudah tersedia pada modul tersebut.

---

### Step 5: Rekonstruksi key dan analisis ciphertext

Key dibuat dengan menggabungkan empat potongan byte:

```python
key = b''.join((b'ARE', b'NA404', b'-KEY', b'-26!'))
```

Hasilnya:

```text
ARENA404-KEY-26!
```

Panjang key adalah **16 byte (128 bit)**, sesuai dengan AES-128. Ciphertext disimpan sebagai string HEX, lalu diubah menjadi bytes menggunakan `bytes.fromhex()` sebelum didekripsi.

Urutan pemulihan plaintext adalah **AES decrypt → hapus PKCS7 padding → decode ASCII**. Karena semua parameter telah ditemukan, flag dapat dipulihkan tanpa perlu memodifikasi atau menamatkan game.

---

### Step 6: Dekripsi ciphertext AES

Install library yang dibutuhkan:

```bash
python -m pip install cryptography
```

Buat file `solver.py` dengan kode berikut.

#### Solver lengkap

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

key = b''.join((b'ARE', b'NA404', b'-KEY', b'-26!'))

ciphertext = bytes.fromhex('d1622e13b67557b28acf0976e608c4e33eb62a3b9bd9e3fdd58d7d017b081b329039f50a453b4d970eb65be908bc2dbf')

decryptor = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
padded = decryptor.update(ciphertext) + decryptor.finalize()

unpadder = PKCS7(128).unpadder()
flag = unpadder.update(padded) + unpadder.finalize()

print(flag.decode())
```

Jalankan:

```bash
python solver.py
```

Output:

```text
LKS{a7f3c91e8b2d4605f0a6c3e9d14b8275}
```

**Hasil:** flag berhasil diperoleh dari ciphertext AES yang tertanam di dalam bytecode Python. Jalur ini merupakan solusi *reverse engineering* melalui ekstraksi, dekompilasi, dan analisis kode, tanpa harus memenangkan game secara langsung.

---

## Flag

```text
LKS{a7f3c91e8b2d4605f0a6c3e9d14b8275}
```
