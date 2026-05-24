# Reading ROT13

Text that looks like English (spaces and punctuation intact) but whose words are gibberish is usually a substitution cipher. The hint here was "Ave Caesar!", a Caesar cipher. Of 25 possible shifts, ROT13 is the most common, and the challenge title was itself the ROT13 encoding of "ROT13". So: ROT13.

```bash
echo "<ciphertext>" | tr 'A-Za-z' 'N-ZA-Mn-za-m'
```

Plaintext drops out.

## Lesson

A non-zero amount of CTF intel hides in the challenge title. Spend ten seconds asking what the name means before you reach for a frequency-analysis tool.
