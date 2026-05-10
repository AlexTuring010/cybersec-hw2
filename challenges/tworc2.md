This challenge uses an encryption scheme that’s basically a **2DES-like construction**, but with **ARC2** and _very short keys_ — only 3 bytes each, zero-padded to 5 bytes.

The encryption function looks like this:

```python
def encrypt(m):
    m_bytes = m.encode()

    cipher1 = ARC2.new(key1.ljust(5, b'\x00'), ARC2.MODE_ECB)
    m_bytes = cipher1.encrypt(m_bytes)

    cipher2 = ARC2.new(key2.ljust(5, b'\x00'), ARC2.MODE_ECB)
    m_bytes = cipher2.encrypt(m_bytes)

    return binascii.hexlify(m_bytes).decode()
```

So basically, the ciphertext is:

$$
\text{ciphertext} = E_{key2}(E_{key1}(\text{plaintext}))
$$

---

At first glance, brute forcing both keys might seem impossible, since it would mean trying $2^{24} \times 2^{24} = 2^{48}$ combinations — way too big.

But there’s a neat trick called the **Meet-in-the-Middle** attack, which reduces the complexity to about $2^{25}$, a much more doable number.

---

### Here’s how the Meet-in-the-Middle attack works:

1. We pick a known plaintext, say `"AAAAAAAA"`.
2. We compute $E_{key1}(\text{"AAAAAAAA"})$ for every possible key1 (that’s $2^{24}$ possibilities), and store all these intermediate results in a dictionary or set for O(1) lookups.
3. Then, knowing the ciphertext of `"AAAAAAAA"` from the service (call it `cipher`), we compute $D_{key2}(\text{cipher})$ for every possible key2 (another $2^{24}$ tries).
4. For each decryption, we check if the result matches one of the stored intermediate encryptions.
5. When a match is found, we have the key1 and key2 that generated the ciphertext!

---

This means the total effort is roughly:

$$
2^{24} + 2^{24} = 2^{25}
$$

which is totally doable on a normal laptop — just takes a bit of patience.

Once you have both keys, decrypting the flag is easy.

---

### Here’s the script I put together to do this:

```python
from Crypto.Cipher import ARC2
import binascii
from tqdm import tqdm

PLAINTEXT = b"AAAAAAAA"

# Put here the ciphertext you get after encrypting PLAINTEXT on the server
CIPHERTEXT_HEX = "a9923e28b4908fec"
CIPHERTEXT = binascii.unhexlify(CIPHERTEXT_HEX)

def pad_key(k3):
    return k3.ljust(5, b'\x00')  # pad 3-byte key to 5 bytes

def build_forward_table():
    table = {}
    print("[*] Building encryption table...")
    for i in tqdm(range(1 << 24), desc="Encrypting with key1"):
        k1 = i.to_bytes(3, 'big')
        cipher1 = ARC2.new(pad_key(k1), ARC2.MODE_ECB)
        mid = cipher1.encrypt(PLAINTEXT)
        table[mid] = k1
    return table

def search_keys(ciphertext, table):
    print("[*] Trying key2 decryptions and matching...")
    for i in tqdm(range(1 << 24), desc="Decrypting with key2"):
        k2 = i.to_bytes(3, 'big')
        cipher2 = ARC2.new(pad_key(k2), ARC2.MODE_ECB)
        mid = cipher2.decrypt(ciphertext)
        if mid in table:
            k1 = table[mid]
            print("\n[+] Keys found!")
            print("key1:", k1.hex())
            print("key2:", k2.hex())
            return k1, k2
    print("[-] No keys found.")
    return None, None

def decrypt_flag(ciphertext, k1, k2):
    cipher2 = ARC2.new(pad_key(k2), ARC2.MODE_ECB)
    cipher1 = ARC2.new(pad_key(k1), ARC2.MODE_ECB)
    mid = cipher2.decrypt(ciphertext)
    plaintext = cipher1.decrypt(mid)
    return plaintext

if __name__ == "__main__":
    forward_table = build_forward_table()
    k1, k2 = search_keys(CIPHERTEXT, forward_table)

    if k1 and k2:
        encrypted_flag_hex = "3059ba4c4514e0678770287f4d2a1bf447aacc2424bf78db6f98ff498f79e801"
        encrypted_flag = binascii.unhexlify(encrypted_flag_hex)
        plaintext = decrypt_flag(encrypted_flag, k1, k2)
        print("\nDecrypted flag:", plaintext.decode())
```

---

I ran it on my slow laptop and it took maybe 40 minutes — probably because I didn’t optimize it and Python isn’t blazing fast — but I got a nice break while waiting, and in the end the flag was:

```
ef647db98f7062a49bda139329caf502
```
