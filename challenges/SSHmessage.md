To solve this challenge I followed the method from this video: [https://www.youtube.com/watch?v=\_lg2AEqRTjg](https://www.youtube.com/watch?v=_lg2AEqRTjg)

Here’s my script:

```python
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

plaintext = m.to_bytes((m.bit_length() + 7) // 8, "big")
print(plaintext)
```

The result was:

```
b'\x02c~\xc5o\x98\x8dzc\x00need_moar_bits!!PJSYA'
```

The tail is readable and says “need_moar_bits!!PJSYA” — looks like a joke about how this RSA key was weak and didn’t use enough bits.
