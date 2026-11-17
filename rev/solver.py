from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

key = b''.join((b'ARE', b'NA404', b'-KEY', b'-26!'))

ciphertext = bytes.fromhex(
    'd1622e13b67557b28acf0976e608c4e3'
    '3eb62a3b9bd9e3fdd58d7d017b081b3'
    '29039f50a453b4d970eb65be908bc2dbf'
)

decryptor = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
padded = decryptor.update(ciphertext) + decryptor.finalize()

unpadder = PKCS7(128).unpadder()
flag = unpadder.update(padded) + unpadder.finalize()

print(flag.decode())
