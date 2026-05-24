# SQLi → leaked hash → cracked password → forged MAC cookie

The interesting part of this one is that the cookie verification compared MAC digests *incorrectly*. Full chain:

1. SQL injection to leak a real username and its salted password hash.
2. Crack the salted hash with rockyou.
3. Forge an admin cookie whose MAC matches in just one byte, because of the verification bug.

## The MAC-truncation bug

Server code:

```python
checks = [lambda a, b: ord(a[i]) ^ ord(b[i]) for i in range(0, 128)]
def safe_hash_cmp(a, b):
    if len(a) != 128 or len(b) != 128:
        return False
    return sum(check(a, b) for check in checks) == 0
```

Classic late-binding closure bug. Every lambda captures the same `i` by reference, so by the time they execute, `i` is 127. The "constant-time compare" actually compares the last character of the digest 128 times and ignores the other 127 positions.

So if you can guess the last hex character of the digest correctly, the function returns `True`. 1-in-16 chance per attempt.

## Getting a real user and hash through SQLi

The login query was string-formatted. Two payloads:

- `' OR 1=1 --` → server's error message echoed the matched username back.
- `' UNION SELECT password, name, admin FROM users WHERE name = '<leaked username>' --` → same trick to echo the hash through the error path.

Salt was hard-coded in the source. Cracked the salted SHA-512 against rockyou.

## Forging the cookie

With the real `name`, `password`, and `admin=1`, the only unknown is the MAC. Iterate over `0123456789abcdef` as the last hex char; one of them is right. Server returns 200 on success.

## Lesson

Late-binding lambdas in Python are a well-known footgun, and they're especially dangerous in security-critical code. "Looks like a constant-time compare" is not the same as "is a constant-time compare". Hash comparison should always go through `hmac.compare_digest` or equivalent.
