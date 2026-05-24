# Forcing a CTR nonce collision through process timing

CTR mode is secure when the nonce is unique per (key, message). This server constructed its nonce from:

- current time (high bits)
- machine MAC address (constant)
- process ID (low bits, easily varied by counter)

Encrypting our own plaintext lets us recover a keystream via known-plaintext, but the next connection picks a fresh nonce, so the keystream changes. Useless on its own. Unless we can engineer two connections whose nonces overlap.

## The race

If we open two connections close enough in time, the *time* portion of the nonce matches. The PIDs differ, so the low bits diverge, but those are counter-style differences, so we can step one session forward to align with the other.

Naive attempts with `gnome-terminal --tab` or sequential `tmux send-keys` had too much startup lag. What worked was launching two `nc` sessions in a single `tmux` script:

```bash
tmux new-session -d "nc <host> <port>"
tmux split-window -h "nc <host> <port>"
tmux attach
```

Then increment the counter in the lower-PID session a few times to align the keystreams.

## Recovering the flag

Once two sessions share a keystream:

1. In session A, encrypt a known plaintext. Recover the keystream: `K = ct_known XOR known`.
2. In session B, encrypt the flag. Recover: `flag = ct_flag XOR K`.

The server in this challenge also folded a seed-hashing step into the keystream, so the final XOR chained `ct_flag XOR ct_seed XOR sha256(seed)`. Standard pattern, just more layers.

## Lesson

Deriving nonces from process timing or PID is fragile. If an attacker can race two requests into the same nonce window, the "unique nonce" assumption that CTR depends on is gone. Once nonces collide, CTR collapses into the two-time-pad scenario where XORing two ciphertexts recovers the XOR of their plaintexts. Use a counter or a CSPRNG, not the clock.
