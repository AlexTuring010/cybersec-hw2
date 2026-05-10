from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse

with open("id_rsa.pub", "r") as f:
    key = RSA.import_key(f.read())

print("n =", key.n)
print("e =", key.e)

p = 1224205479305284153071710427590269741
q = 51062656435577845003667627259245966557039

n = p * q
e = key.e
phi = (p - 1) * (q - 1)
d = inverse(e, phi)

with open("flag.enc", "rb") as f:
    ciphertext = f.read()

c = int.from_bytes(ciphertext, "big")
m = pow(c, d, n)

print(plaintext)