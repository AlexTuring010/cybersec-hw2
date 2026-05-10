import base64
import json

def b64decode(s):
    s += '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s.encode())

def b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip('=')

def modify_token(token: str, new_payload: dict) -> str:
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid token format")

    header, sig = parts[1], parts[2]

    # Encode new payload to base64
    new_payload_bytes = json.dumps(new_payload, separators=(',', ':')).encode()
    new_payload_b64 = b64encode(new_payload_bytes)

    # Rebuild token with original header + sig
    tampered_token = f'{new_payload_b64}.{header}.{sig}'
    return tampered_token

# === Example usage ===
original_token = 'eyJhZG1pbiI6MCwidGljayI6MiwidXNlciI6IkFsZXhUdXJpbmcifQ.aDZoGg.n0YnjA5IBjDyz9exTZkDkEcegw4'

# 🔧 Define your custom payload here
custom_payload = {
    "admin": 0,
    "tick": 10,
    "user": "AlexTuring"
}

tampered_token = modify_token(original_token, custom_payload)

print(f'Tampered token:\n{tampered_token}')
