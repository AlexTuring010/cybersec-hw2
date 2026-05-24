# Brute-forcing a nested steg chain with stegseek

This one cost me hours of dead-end stego analysis. I tried LSB tools, spectrogram analysis (convinced for a while that there were hidden letters in there; there weren't), and every stego tool I could find online.

What finally worked: `stegseek` with `rockyou.txt` against the original audio file.

```bash
stegseek <input.wav> rockyou.txt
```

That extracted an embedded JPEG. Ran stegseek again on the JPEG:

```bash
stegseek <extracted.jpg> rockyou.txt
```

Out came a text file with the flag string.

The actual lesson cost me an extra hour separately: I submitted the flag without its trailing `!` first, thinking the punctuation was just emphasis. It wasn't. Re-submitted with the exact string, accepted.

## Lessons

1. Before you try anything clever in stego, try `stegseek` with rockyou. A large fraction of CTF steg challenges use dictionary passwords with `steghide`.
2. Submit flags exactly as printed. Don't strip punctuation. Don't add or remove whitespace. CTF flag comparison is almost always a byte-for-byte string match.
