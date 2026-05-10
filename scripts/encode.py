import base64
import sys

if len(sys.argv) != 2:
    print("Usage: python decode.py <base64_string>")
    sys.exit(1)

data = sys.argv[1]

decoded = base64.b64decode(data).decode()
print("Decoded string:", decoded)
