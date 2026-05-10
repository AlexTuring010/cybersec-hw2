from binascii import unhexlify

# Given data
data = b'Xr\xacR0\xf4\xc8\xac|\xffmt\xc4A{\x03s\xef\x9c\x96[\xf1\x11\xec\x80\xba\x08\xb3.a\x1du\xaa'

# Extract the first 16 bytes
first_16_bytes = data[:16]

# Hex strings to XOR with
hex_string_1 = "3c27108f35c4f9fe4ad4c5295ab4857d"
hex_string_2 = "6e5ab3d20a3f3e5d3924a75291faf171"

# Convert hex strings to bytes
xor_bytes_1 = unhexlify(hex_string_1)
xor_bytes_2 = unhexlify(hex_string_2)

# XOR all three byte sequences together
result = bytes(a ^ b ^ c for a, b, c in zip(first_16_bytes, xor_bytes_1, xor_bytes_2))

# Decode the result to ASCII
ascii_result = result.decode('ascii') 

print("XOR result (ASCII):", ascii_result)