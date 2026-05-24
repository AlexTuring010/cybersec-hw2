# Two-time pad on images

The server encrypted two BMP images with XOR using the *same* keystream `K`:

```
ct1[i] = pt1[i] XOR K[i]
ct2[i] = pt2[i] XOR K[i]
```

XORing the two ciphertexts cancels the key:

```
ct1[i] XOR ct2[i] = pt1[i] XOR pt2[i]
```

You don't get either plaintext directly, but XOR'd images are extremely forgiving. Edges, shapes, large solid regions all survive, and human eyes are great at reading them through that noise.

## BMP gotcha

BMP files have a ~54-byte header you need to keep intact. XOR only the pixel data.

```python
def xor_bmp_pixels(file1, file2, output):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        d1, d2 = f1.read(), f2.read()
    offset = int.from_bytes(d1[10:14], 'little')
    pixels = bytes(a ^ b for a, b in zip(d1[offset:], d2[offset:]))
    with open(output, 'wb') as out:
        out.write(d1[:offset] + pixels)
```

The XOR'd image was readable enough that the flag text rendered visibly in the output.

## Lesson

A one-time pad reused is just a pad. Once the same key encrypts two messages, an XOR collapses both back into a recoverable form. The "one-time" part of "one-time pad" is the only thing keeping it secure. Once it stops being one-time, you're closer to plaintext than ciphertext.
