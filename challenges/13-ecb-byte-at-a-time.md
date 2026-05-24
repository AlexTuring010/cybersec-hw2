# ECB byte-at-a-time recovery

The server encrypts a message of the form:

```
f"agent {agent} wants to see {flag}"
```

with AES in ECB mode, where we control `agent` and the goal is to recover `flag`.

ECB's defining weakness: identical 16-byte plaintext blocks always produce identical ciphertext blocks under the same key. That's the whole attack.

## Step 1: pin down the flag length

By feeding increasing lengths of `agent` and watching when the ciphertext grows by another 16-byte block, you can back out the flag length from the known padding rule. (Worth being precise about the padding here: the server in this challenge always appended a `'1'` first, then zero-padded up to a block boundary, so the "padding only adds zero bytes" intuition is wrong.)

## Step 2: recover one byte at a time

The idea:

- Pad `agent` so the *last* block before the flag is `[15 unknown padding bytes][1 target flag byte]`.
- Replicate the same `[15 padding bytes][1 guess byte]` pattern in an attacker-controlled block earlier in the message.
- For each candidate byte (0-255), check whether the controlled block's ciphertext matches the target block's ciphertext. Match = correct byte.

Repeat, shifting the boundary by one each round, recovering one byte per server interaction. The script is a nested loop: outer over flag positions, inner over candidate bytes.

## Why this works

ECB encrypts each 16-byte block independently with the same key. If you can arrange two plaintext blocks to be identical except for the one byte you want to learn, ECB tells you (via ciphertext equality) when you've guessed right. No key recovery required.

## Lesson

ECB has no place encrypting structured data, especially data the attacker partially controls. The fact that you can detect plaintext equality through the ciphertext is enough to leak any controlled content one byte at a time. The fix is any mode that adds per-block randomness: CBC with a real IV, CTR with a unique nonce, GCM.
