# cybersec-hw2

Homework #2 for *Introduction to Computer Security* at the University of Athens (Department of Informatics & Telecommunications).

The web & cryptography half of the class HackCenter ladder — SQL injection, cookie forging, ECB attacks, Vigenère, RC2, two-time-pad, and a handful of broken-auth puzzles.

> **Solved every challenge. Finished 3rd on the class leaderboard.**

What got me there wasn't raw skill, it was *not giving up*. Most challenges had a wall I had to push through; the post-mortem write-ups in [`challenges/`](challenges/) document each one.

## What's in this repo

- **[`challenges/`](challenges/)** — one Markdown write-up per challenge. All in English. Includes screenshots where they help (CBC mode, decrypted images, server responses, etc.).
- **[`scripts/`](scripts/)** — the Python tooling I built to crack the harder ones. A bit of a workshop drawer — payload generators, decryption helpers, brute-forcers, and a couple of bespoke clients.

## Favourite challenges

### 1. The Facebook 1

The one that made me feel like an actual hacker. The injection point everyone tried was the form fields — the *real* one was inside the like-button ID. I built a small console tool that uses **blind SQL injection** to extract a target's password one character at a time, with a tiny live UI. Most rewarding solve of the homework.

### 2. Cloudz

Source code was provided — no more blind probing. Three steps:

1. **SQL injection** to leak a hash via error messages.
2. **Crack the hash** — but not to log in.
3. **Forge an admin cookie** with the cracked secret.

The trick: the server only verified the *last character* of the signature. No need to brute-force the whole MAC.

### 3. BrokenEncryption0

A textbook **ECB byte-at-a-time** attack — but I wrote it from scratch as a precise, well-instrumented script that pulls the flag one character at a time. The challenge writeup in `challenges/` walks through why ECB leaks structure.

### 4. tworc2

A chained-RC2 setup where the same cipher object normally can't both encrypt and decrypt back-to-back — except this implementation could. Once I understood the state machine, I crafted a block-by-block decryption that drops the flag straight out.

### Honourable mention — The Facebook 2

Worth the most points on the board, but it only took two payloads once I found the injection point (the error page). Most people gave up before they spotted it.

## License

[MIT](LICENSE) — applies to my own work in this repo (writeups, scripts, exploits). Class-distributed source/binaries retain their original course copyright.

## Sequence

Part of a five-piece cybersecurity coursework cluster:

1. [cybersec-bn0](https://github.com/AlexTuring010/cybersec-bn0) — class warm-up
2. [cybersec-hw0](https://github.com/AlexTuring010/cybersec-hw0) — first homework
3. [cybersec-hw1](https://github.com/AlexTuring010/cybersec-hw1) — HackCenter binary exploitation (1230 points)
4. **cybersec-hw2** *(you are here)* — HackCenter web & crypto (3rd place)
5. [cybersec-hw3-chimera-agents](https://github.com/AlexTuring010/cybersec-hw3-chimera-agents) — team CTF capstone
