import hashlib

salt = b'no_google_for_you'
target_hash = "3dbaf7a06a402ef22ab9a1e0f14b3e861cacc324ba8ffc6b6d985fc843b1e4d3366fc31f6d47fedfa58781b845721b6a0403df44eb1baba8c00b1befd088ec2e"

with open('./../../rockyou.txt', 'rb') as f:
    for line in f:
        password = line.strip()
        attempt = hashlib.sha512(salt + password).hexdigest()
        if attempt == target_hash:
            print(f"Password found: {password.decode()}")
            break