def xor_bmp_pixels(file1, file2, output_file):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()

    # BMP header is typically 54 bytes (but safer to read offset from header)
    # The pixel data offset is stored at bytes 10-13 (4 bytes, little-endian)
    pixel_offset = int.from_bytes(data1[10:14], byteorder='little')

    if len(data1) != len(data2):
        raise ValueError("Files must be the same size!")

    # Extract headers (unchanged)
    header = data1[:pixel_offset]

    # Extract pixel data
    pixels1 = data1[pixel_offset:]
    pixels2 = data2[pixel_offset:]

    if len(pixels1) != len(pixels2):
        raise ValueError("Pixel data lengths do not match!")

    # XOR pixel data
    xor_pixels = bytes([b1 ^ b2 for b1, b2 in zip(pixels1, pixels2)])

    # Combine header + XORed pixels
    xor_data = header + xor_pixels

    # Write output
    with open(output_file, 'wb') as out:
        out.write(xor_data)

    print(f"XOR image saved as {output_file}")

xor_bmp_pixels("enc1.bmp", "enc2.bmp", "xor_output.bmp")
