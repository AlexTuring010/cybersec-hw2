# RSA with an undersized modulus

The challenge gave a small RSA public key and a ciphertext. With `n` only a few hundred bits, factoring it into `p` and `q` is feasible with standard tooling: online factor databases (`factordb`), or `msieve`/`cado-nfs` on a laptop for the slightly larger end of "small".

Once you have `p`, `q`, and `e`, the rest is textbook:

```python
from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse

key = RSA.import_key(open("pub.key").read())
n, e = key.n, key.e

p, q = <factored>  # from external tooling
phi = (p - 1) * (q - 1)
d = inverse(e, phi)

c = int.from_bytes(open("ct.bin", "rb").read(), "big")
m = pow(c, d, n)
print(m.to_bytes((m.bit_length() + 7) // 8, "big"))
```

The decrypted plaintext for this challenge ends with text the challenge author wrote (roughly "needs more bits"), basically the puzzle's own commentary on the weak key.

## Lesson

RSA's security comes from the cost of factoring `n`. If `n` fits in a couple hundred bits, none of the rest of the protocol matters. Your padding scheme is irrelevant, your `e` is irrelevant, the cleverness of your application is irrelevant. Use 2048-bit moduli at minimum, 3072+ for anything long-lived.
