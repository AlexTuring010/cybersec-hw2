## Two-Time Pad (More Like Two-Time Fail)

If you're worried about running out of keys, then congratulations, you’ve just invented the world’s **worst** cost-saving scheme.

You really thought using the **same key twice** makes your "two-time pad" **twice as secure**? No, what you actually did was **break one of the most fundamental rules in cryptography**, slap a name on it, and call it innovation.

You gave us two encrypted images. According to your scheme:

```
encrypted_pixels1[i] = pixels1[i] XOR K[i]
encrypted_pixels2[i] = pixels2[i] XOR K[i]
```

Now, I don’t need to be an expert in cryptography to realize that:

```
encrypted_pixels1[i] XOR encrypted_pixels2[i] = pixels1[i] XOR pixels2[i]
```

Sure, from `pixels1[i] XOR pixels2[i]`, I can't directly tell what each original pixel was. But here’s the thing: **this still leaks information**. In fact, **a lot** of information, especially when we're dealing with images. I don’t need a perfect reconstruction. Images are very forgiving: edges, shapes, and transitions often survive the XOR.

So I gave it a shot.

---

### BMP Format 101

Turns out BMP files have a header, typically 54 bytes, and **you didn't encrypt it**. Which means I need to preserve the header and XOR only the pixel data.

Here's the script I whipped up:

```python
def xor_bmp_pixels(file1, file2, output_file):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    # Read pixel data offset (bytes 10-13, little-endian)
    pixel_offset = int.from_bytes(data1[10:14], byteorder='little')

    if len(data1) != len(data2):
        raise ValueError("Files must be the same size!")

    header = data1[:pixel_offset]
    pixels1 = data1[pixel_offset:]
    pixels2 = data2[pixel_offset:]

    if len(pixels1) != len(pixels2):
        raise ValueError("Pixel data lengths do not match!")

    xor_pixels = bytes([b1 ^ b2 for b1, b2 in zip(pixels1, pixels2)])
    xor_data = header + xor_pixels

    with open(output_file, 'wb') as out:
        out.write(xor_data)

    print(f"XOR image saved as {output_file}")

xor_bmp_pixels("enc1.bmp", "enc2.bmp", "xor_output.bmp")
```

---

### Result?

Behold, the glorious product of your “enhanced” encryption scheme:

![xor_output](./decrypted_image.png)

The **flag just popped out**.

Next time, maybe don’t try to patent a cryptographic disaster.
