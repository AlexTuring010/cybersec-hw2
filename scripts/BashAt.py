def atbash(text):
    result = []
    for char in text:
        if char.isupper():
            result.append(chr(ord('Z') - (ord(char) - ord('A'))))
        elif char.islower():
            result.append(chr(ord('z') - (ord(char) - ord('a'))))
        else:
            result.append(char)
    return ''.join(result)

# Read file and decode
with open("BashAt.txt", "r") as f:
    ciphertext = f.read()

decoded = atbash(ciphertext)
print(decoded[:1000])  # Preview the decoded output
