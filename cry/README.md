# CRYPTOGRAPHY

## Author

Nikoo

## Categories

Cryptography

## Description

Flag format: `LKS{...}`

## Attachment

- `chall.py`
- `output.txt` (berisi `n` dan 37 buah ciphertext `c`)

## Solver

### Step 1: Analisis source code

Fungsi `buat_kunci()` membuat modulus `n = p * q` dari dua prima 512-bit dengan `e = 65537`. Sampai sini tidak ada yang aneh: `n` 1024-bit, jadi faktorisasi tidak realistis.

Yang menarik ada di fungsi `enkripsi()`:

```python
def enkripsi(pesan, modulus, eksponen):
    ciphertext = [
        enkripsi_satu_byte(nilai_byte, eksponen, modulus)
        for nilai_byte in pesan
    ]
    return ciphertext
```

Flag dienkripsi **satu byte per satu byte** dengan `c_i = m_i^e mod n`, tanpa padding (bukan OAEP/PKCS#1) dan tanpa unsur acak.

**Hasil:** Enkripsinya bersifat **deterministik**: byte yang sama akan selalu menghasilkan ciphertext yang sama. Ini terlihat jelas di `output.txt`: dari 37 ciphertext, hanya ada 21 nilai unik, karena karakter yang berulang menghasilkan angka yang persis sama. Selain itu, ruang plaintext per blok cuma 256 kemungkinan (0-255), jadi sebenarnya ini cuma *substitution cipher* biasa dengan 256 simbol.

---

### Step 2: Susun lookup table (dictionary attack)

Karena `n` dan `e` itu publik, kita bisa mengenkripsi sendiri semua 256 kemungkinan byte dan membuat tabel pemetaan ciphertext -> byte:

```python
lookup = {
    pow(byte, e, n): byte
    for byte in range(256)
}
```

Tidak perlu faktorisasi `n`, tidak perlu mencari `d`. Cukup 256 kali `pow()`.

**Hasil:** Setiap ciphertext di `output.txt` tinggal dicocokkan dengan tabel ini untuk mendapatkan byte aslinya.

---

### Step 3: Dekripsi seluruh ciphertext

Parse 37 ciphertext dari `output.txt`, lalu cari satu per satu di `lookup`:

```python
c = list(map(int, c.split()))
plaintext = bytes(lookup[nilai] for nilai in c)
flag = plaintext.decode("utf-8")
```

Sanity check: ciphertext pertama sampai keempat ter-decode menjadi `L`, `K`, `S`, `{`, sesuai format flag, dan ciphertext terakhir menjadi `}`.

---

### Solver lengkap

```python
# n = modulus RSA dari challenge
# e = 65537
# c = """list 37 ciphertext dari challenge"""

c = list(map(int, c.split()))
lookup = {
    pow(byte, e, n): byte
    for byte in range(256)
}

plaintext = bytes(lookup[nilai] for nilai in c)
flag = plaintext.decode("utf-8")

print(f"Jumlah ciphertext : {len(c)}")
print(f"Flag              : {flag}")
```

Output:

```
Jumlah ciphertext : 37
Flag              : LKS{a7f3c91e5b2d8046f1a9c73e8d0b6254}
```

---

## Flag

```
LKS{a7f3c91e5b2d8046f1a9c73e8d0b6254}
```
