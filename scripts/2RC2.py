#!/usr/bin/env python3

from Cryptodome.Cipher import ARC2
import os
import string
import random
import binascii

# You do not have access to the flag file.
try:
    with open("flag", "r") as f:
        flag = f.read().strip()
except FileNotFoundError:
    flag = "PLACEHOLDER_FLAG"  # For testing

master_key = bytes.fromhex(''.join(random.choice(string.digits + 'abcdef') for _ in range(12)))
key1 = master_key[:3]
key2 = master_key[3:]


def encrypt(m):
    m_bytes = m.encode()

    cipher1 = ARC2.new(key1.ljust(5, b'\x00'), ARC2.MODE_ECB)
    m_bytes = cipher1.encrypt(m_bytes)

    cipher2 = ARC2.new(key2.ljust(5, b'\x00'), ARC2.MODE_ECB)
    m_bytes = cipher2.encrypt(m_bytes)

    return binascii.hexlify(m_bytes).decode()

welcome = """
*******************************************
***             Welcome to the          ***
***    FlAg EnCrYpTiOn SeRviCe 7006!    ***
*******************************************

We encrypt the flags, you get the points!"""

print(welcome)

m = "To prove how secure our service is, "
m += "here is an encrypted flag:\n"
m += "==================================\n"
m += encrypt(flag)
m += "\n==================================\n"
m += "Find the plaintext and we'll give you points\n"

print(m)

while True:
    try:
        m = input("\nNow enter a message you wish to encrypt: ")
        if len(m) % 8 == 0:
            print("Your super unreadable ciphertext is:")
            print("==================================")
            print(encrypt(m))
            print("==================================")
        else:
            print("Your message's length should be a multiple of 8")
    except EOFError:
        break

