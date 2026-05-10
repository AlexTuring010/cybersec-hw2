from Crypto.Cipher import ARC2
import itertools
import binascii
from tqdm import tqdm 

# Your known plaintext
PLAINTEXT = b"AAAAAAAA"

# Replace with the ciphertext you got back from the server when you submitted "AAAAAAAA"
CIPHERTEXT_HEX = "a9923e28b4908fec"
CIPHERTEXT = binascii.unhexlify(CIPHERTEXT_HEX)

def pad_key(k3):
    return k3.ljust(5, b'\x00')  # pad 3-byte key to 5 bytes

def build_forward_table():
    table = {}
    print("[*] ")
    for i in tqdm(range(1 << 24), desc="Building encryption table...", ncols=80) :
        k1 = i.to_bytes(3, 'big')
        cipher1 = ARC2.new(pad_key(k1), ARC2.MODE_ECB)
        mid = cipher1.encrypt(PLAINTEXT)
        table[mid] = k1
    return table

def search_keys(ciphertext, table):
    for i in tqdm(range(1 << 24), desc="Brute-forcing key2 and matching...", ncols=80):
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
        # Now decrypt the real flag from the printed ciphertext
        encrypted_flag_hex = "3059ba4c4514e0678770287f4d2a1bf447aacc2424bf78db6f98ff498f79e801"
        encrypted_flag = binascii.unhexlify(encrypted_flag_hex)
        plaintext = decrypt_flag(encrypted_flag, k1, k2)
        print("\nDecrypted flag:", plaintext.decode())
