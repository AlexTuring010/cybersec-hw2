# cybersec-hw2

Homework #2 for *Introduction to Computer Security* at the University of Athens (Department of Informatics and Telecommunications).

The web and cryptography half of the class CTF ladder: SQL injection, server-side template injection, ECB and CBC attacks, classical ciphers, two-time pad, meet-in-the-middle on double encryption, broken MAC comparison, and a handful of broken-auth puzzles.

> **Solved every challenge. Finished 3rd on the class leaderboard.**

What carried me wasn't raw skill, it was *not giving up*. Most of these had a wall I had to push through before the solution clicked. Each writeup in [`challenges/`](challenges/) documents the dead ends as well as the working approach.

## What's in this repo

- [`challenges/`](challenges/): one Markdown writeup per technique. Each one explains the bug class, the reasoning, and the structure of the attack, without literal flag values, hostnames, or runnable exploit scripts. Those were removed deliberately so this stays a writeup collection rather than a copy-paste cheat sheet for future class iterations.

## A few I'm proud of

- **Blind SQLi through a non-obvious parameter.** The visible login form was hardened. The actual injection point was an AJAX ID field nobody filtered. Recovered a 31-character password one byte at a time using boolean response oracles.
- **SQLi to hash crack to forged MAC cookie.** Three-stage chain where the cookie verification had a closure-capture bug that effectively only checked one byte of the MAC.
- **ECB byte-at-a-time recovery.** Textbook attack, but writing the script from scratch with precise block alignment was the real lesson.
- **Meet-in-the-middle on a 2DES-style double encryption with short keys.** Brought a `2^48` brute-force down to `2^25` by trading memory for time.
- **SSTI through an error page.** Most rewarding solve in terms of "the bug was hiding in plain sight". Every other student probed the welcome page and stopped there.

## License

[MIT](LICENSE) applies to my own work in this repo (writeups). Class-distributed source and binaries retain their original course copyright.

## Sequence

Part of a five-piece cybersecurity coursework cluster:

1. [cybersec-bn0](https://github.com/AlexTuring010/cybersec-bn0): class warm-up
2. [cybersec-hw0](https://github.com/AlexTuring010/cybersec-hw0): first homework
3. [cybersec-hw1](https://github.com/AlexTuring010/cybersec-hw1): binary exploitation ladder (1230 points)
4. **cybersec-hw2** *(you are here)*: web and cryptography ladder (3rd place)
5. [cybersec-hw3-chimera-agents](https://github.com/AlexTuring010/cybersec-hw3-chimera-agents): team CTF capstone
