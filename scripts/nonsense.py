#!/usr/bin/python3 -u
from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
from Cryptodome.Util import Counter

from binascii import hexlify, unhexlify
import time, os, uuid

def raw(x):
  return bytes(map(lambda y:y if isinstance(y,int) else ord(y),x))

flag = raw(open("./flag.txt").read())

nonce  = (int(time.time()) << (48 + 16)) | (int(uuid.getnode()) << 16) | (int(os.getpid()))

counter = Counter.new(128, initial_value=nonce)
cryptor = AES.new(raw(SHA256.new(flag).digest()), AES.MODE_CTR, counter=counter)

def choose():
  return input("Your choice: ")

def send_flag():
  print(hexlify(cryptor.encrypt(flag)))

def send_n_rand_bytes(seed, nb):
  output = b''
  for i in range(0, nb, 32):
    seed = SHA256.new(raw(seed)).digest()
    output += hexlify(cryptor.encrypt(seed[0:min(nb-i,32)]))
  print(output)

while True:
  print("Commands: (f)lag or (r)andom")
  choice = choose()
  if choice == "f":
    print("Okay, here is the flag: ")
    send_flag()
  elif choice == "r":
    seed = SHA256.new(raw(flag+SHA256.new(flag).digest())).digest()
    print("Would you like to provide an RNG seed? (y)es or (n)o?")
    choice = choose()
    if choice == 'y':
      while True:
        hseed = input("RNG seed as hex: ")
        if len(hseed)&1:
          print("Could not decode RNG seed")
        else:
          try:
            seed = unhexlify(hseed)
            break
          except binascii.Error:
            print("Could not decode RNG seed")
    elif choice != 'n':
      print("Not sure what you meant by that, we'll assume that means no...")

    while True:
      nb = input("How many bytes of random output do you want? ")
      try:
        nb = int(nb)
        break
      except ValueError:
        print("Sorry, didn't understand that")

    send_n_rand_bytes(seed, nb)
      
  else:
    print("That's not one of the options")
    break
