from math import gcd
from Crypto.Util.number import getPrime

def buat_kunci():
    eksponen = 65537

    while True:
        prima_pertama = getPrime(512)
        prima_kedua = getPrime(512)

        if prima_pertama == prima_kedua:
            continue

        modulus = prima_pertama * prima_kedua
        totient = (prima_pertama - 1) * (prima_kedua - 1)

        if gcd(eksponen, totient) == 1:
            return modulus, eksponen


def enkripsi_satu_byte(nilai_byte, eksponen, modulus):
    return pow(nilai_byte, eksponen, modulus)


def enkripsi(pesan, modulus, eksponen):
    ciphertext = [
        enkripsi_satu_byte(nilai_byte, eksponen, modulus)
        for nilai_byte in pesan
    ]

    return ciphertext

flag = "LKS{***************}"

pesan = flag.encode("utf-8")

modulus, eksponen = buat_kunci()

ciphertext = enkripsi(pesan, modulus, eksponen)

print(f"n = {modulus}")
print(f"e = {eksponen}")
print("ciphertext =")
print(" ".join(map(str, ciphertext)))
