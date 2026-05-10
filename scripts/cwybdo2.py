#!/usr/bin/python3 -u
from Cryptodome.Cipher import AES, ARC4
from Cryptodome.Hash import SHA256
from binascii import hexlify, unhexlify
import os, random

flag = bytes(open("./flag.txt").read(), 'ascii')

arc4_gen = ARC4.new(SHA256.new(flag).digest())

def pad(s, blocksize=16):
  rounded_up = (len(s)//blocksize + 1)*blocksize
  num_pads   = rounded_up - len(s)
  return s.ljust(rounded_up, (num_pads).to_bytes(1, 'big'))

def unpad(s, blocksize=16):
  if not (len(s)%blocksize == 0, len(s)>0):
    print("Messages must be n>1 blocks")
    return None
  num_pads = s[-1]
  if not isinstance(num_pads, int):
    num_pads = ord(s[-1])
  return s[:-num_pads]

class Encryptor(object):
  def __init__(self):
    self.cryptor = None

  def new(self, mode, keysize):
    key = os.urandom(keysize)
    iv  = os.urandom(16)
    modes = {'CBC':AES.MODE_CBC,
             'ECB':AES.MODE_ECB,
             'OFB':AES.MODE_OFB}
    if mode in ["CBC","CFB","OFB"]:
      print("Your (hex encoded) iv is: %s"%hexlify(iv))
      self.cryptor = AES.new(key, IV=iv, mode=modes[mode])
    else:
      self.cryptor = AES.new(key, mode=modes[mode])

  def enc(self, s):
    return self.cryptor.encrypt(pad(s, self.cryptor.block_size))

  def dec(self, s):
    if len(s)%self.cryptor.block_size or len(s)<=0:
      print("ERROR: messages must be n>1 blocks")
      return None
    pt = self.cryptor.decrypt(s)
    if flag.lower() in pt.lower():
      print("ERROR: cannot print out the flag")
      return None
    return unpad(pt, self.cryptor.block_size)

def test_random():
  rs = input("Random source? (o)s, (a)rc4, or (p)ython random\n")
  if not rs or rs[0] not in "oap":
    print("Invalid random source")
    return None
  le = input("How many bytes of randomness do you want?\n")
  try:
    le = int(le, 0)
  except ValueError:
    print("Invalid length")
    return None

  if le > 4096:
    print("Length too large, clipped to 4096")
    le = 4096
  if le < 0:
    print("Invalid length, less than 0")
    return None

  if rs[0] == 'o':
    return os.urandom(le)
  elif rs[0] == 'a':
    return arc4_gen.encrypt("A"*le)
  elif rs[0] == 'p':
    return b"".join((random.getrandbits(8)).to_bytes(1, 'big') for _ in range(le))

def test_enc():
  pt = input("Please input your data here:\n")
  try:
    pt = unhexlify(pt)
  except TypeError:
    print("Could not decode as hex, assuming input is not encoded")
  return pt

def test_dec():
  ct = input("Please enter the data as hex\n")
  try:
    ct = unhexlify(ct)
  except ValueError:
    print("ERROR: data must be given as hex encoded input")
    return None
  return ct

def help():
  print("Welcome to the encryption testbench!")
  print("You have several tools/commands at your disposal:")
  print(" (h)elp")
  print(" (c)reate new cryptor")
  print(" (e)ncrypt")
  print(" (d)ecrypt")
  print(" (r)andom")
  print(" (p)ad")
  print(" (u)npad")

def main_loop():
  bad = 0
  e = Encryptor()

  while True:
    r = input("What would you like to do?\n")
    options = "edchrpu"
    if not r or r[0] not in options:
      if bad > 3:
        print("You don't follow directions. Exiting")
        return
      print("Sorry, I didn't understand that. Please type 'h' for help")
      bad += 1
      continue

    if r[0] == 'h':
      help()
    elif r[0] == 'c':
      print("What cipher mode of operation would you like to use?")
      r = input("Options: (c)bc, (e)cb, (o)fb\n")
      modes = {'c':'CBC'}
      if r and r[0] in modes:
        le = input("How many bytes long should the key be (must be 16, 24, or 32)\n")
        try:
          le = int(le, 0)
          if le not in (16, 24, 32):
            print("ERROR: invalid key size")
          else:
            e.new(modes[r[0]], le)
            print("Successfully updated the encryptor")
        except ValueError:
          print("ERROR: could not convert that to an integer")
      else:
        print("ERROR: invalid cipher mode (note: only CBC mode implemented)")

      
    elif r[0] == 'e':
      if e.cryptor is None:
        print("Sorry, you must (c)reate a new cryptor before you can encrypt messages")
      else:
        print("What would you like to encrypt?")
        r = input("(r)andom, (f)lag, or (c)ustom data?\n")
        if not r or r[0] not in "rfc":
          print("Sorry, that wasn't one of the options")
          continue
        if r[0] == 'r':
          dat = test_random()
        elif r[0] == 'f':
          dat = flag
        elif r[0] == 'c':
          dat = test_enc()
        if dat is not None:
          ed = e.enc(dat)
          if ed:
            print("ENCRYPTED DATA:")
            print(hexlify(ed))
          else:
            print("ERROR: could not encrypt data")
    elif r[0] == 'd':
      if e.cryptor is None:
        print("Sorry, you must (c)reate a new cryptor before you can decrypt messages")
      else:
        dat = test_dec()
        if dat is not None:
          dd = e.dec(dat)
          if dd is None:
            print("ERROR: could not decrypt data")
          else:
            print("DECRYPTED DATA:")
            print(dd)
    elif r[0] == 'r':
      dat = test_random()
      if dat is not None:
        print("RANDOM DATA:")
        print(hexlify(dat))
    elif r[0] == 'p':
      dat = test_dec()
      if dat is not None:
        u = pad(dat)
        if u is None:
          print("ERROR: could not pad that data")
        else:
          print("PADDED DATA:")
          print(hexlify(u))
    elif r[0] == 'u':
      dat = test_dec()
      if dat is not None:
        u = unpad(dat)
        if u is None:
          print("ERROR: could not unpad that data")
        else:
          print("UNPADDED DATA:")
          print(hexlify(u))

if __name__ == "__main__":
  main_loop()
