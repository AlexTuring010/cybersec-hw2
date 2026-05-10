def to_uint8array(s):
    # Interpret escape sequences like \x00 properly
    # First decode the escaped sequences
    decoded = bytes(s, "utf-8").decode("unicode_escape").encode("latin1")
    # Convert to hex byte values
    hex_bytes = [f"0x{b:02x}" for b in decoded]
    # Format as Uint8Array.from([...])
    return f"Uint8Array.from([{', '.join(hex_bytes)}])"

# Example
input_str = r'admin\x00\x00\x00","password":"LEAK'
print(to_uint8array(input_str))
