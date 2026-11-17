# n = modulus RSA dari challenge
# e = 65537
# c = list 37 ciphertext dari challenge

lookup = {
    pow(byte, e, n): byte
    for byte in range(256)
}

plaintext = bytes(lookup[nilai] for nilai in c)
flag = plaintext.decode("utf-8")

print(f"Jumlah ciphertext : {len(c)}")
print(f"Flag              : {flag}")
