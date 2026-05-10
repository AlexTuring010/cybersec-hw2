from binascii import unhexlify
from Cryptodome.Hash import SHA256

def raw(x):
    return bytes(map(lambda y: y if isinstance(y, int) else ord(y), x))

# Server outputs
encrypted_flag_hex = "f6c647021db39ebb264c55dbe133c5910a8d1be51b5f34483254f8e2f523b4343a"
encrypted_seed_hex = "724e876699209f125d6006a0190291978feadbbd351c496d35fb1aa504159d7fd5"

# Seed as a hex string
seed_hex = "AA"

# Convert hex outputs to bytes
encrypted_flag = unhexlify(encrypted_flag_hex)
encrypted_seed = unhexlify(encrypted_seed_hex)
seed = unhexlify(seed_hex)

# Compute hashed seed
hashed_seed = SHA256.new(raw(seed)).digest()
hased_seed2 = SHA256.new(raw(hashed_seed)).digest() # Because we asked for output of 33 bytes if you check nonsense.py
hashed_seed += hased_seed2[0:1]                     # This is how its done, turns out the last character of the flag is just a newline though

# Recover the flag
flag = bytes([ef ^ es ^ hs for ef, es, hs in zip(encrypted_flag, encrypted_seed, hashed_seed)])
print("Recovered flag (hex):", flag.hex())

# Attempt to decode the flag to characters
try:
    decoded_flag = flag.decode("utf-8")
    print("Recovered flag (decoded):", decoded_flag)
except UnicodeDecodeError:
    print("Recovered flag could not be decoded to UTF-8 characters.")