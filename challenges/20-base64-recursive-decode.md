# Recursive Base64 decode

A long string of letters with `=` padding at the end is almost always Base64. The challenge name ("Encode") implied encoding rather than encryption (no key needed). The hint suggested the message had been encoded more than once.

```bash
echo "<ciphertext>" | base64 -d | base64 -d | base64 -d
```

After three rounds, plaintext.

## Lesson

Padding shapes (`=`, `==`) and a `[A-Za-z0-9+/]` charset are Base64 tell-tales. If the decoded result still looks like Base64, decode again. Most CTF "stack of encodings" puzzles bottom out in two or three layers.
