# Decrypting CBC blocks through a stateful oracle

The server gave us a CBC-mode encryption/decryption oracle. Strangely, the same AES object was being used for both encrypt and decrypt operations back-to-back, which most crypto libraries explicitly disallow but this one didn't. That's the hole.

## The CBC chaining state

In CBC, decryption XORs each decrypted block with the previous ciphertext block (or the IV for the first block):

![CBC Mode](CBC.png)

The library kept an internal "last block" used for that XOR. After an encryption, the internal "last block" became the last ciphertext block produced, even though the next operation might be a decryption.

So if you encrypt some throwaway data, then ask the oracle to decrypt a payload, the chaining XOR uses *your last encryption's ciphertext* as the implicit IV, not the IV you'd expect.

## Recovering the flag block by block

1. Encrypt a padded throwaway (e.g. `"AA"`). Call its ciphertext `C_AA`. Internal "last block" is now the last block of `C_AA`.
2. Encrypt the flag. The IV the server used was `C_AA`.
3. Craft a decryption payload `[flag_block_i][IV][C_AA]`. The last block being `C_AA` means the padding check passes (since `C_AA` is the ciphertext of a properly padded block).
4. The first decrypted block is `flag_block_i XOR (last block of payload) XOR (internal "last block")`. Algebra you can solve for `flag_block_i`.

Repeat per flag block. The flag was three blocks long; the last was just padding.

> Side note: the server filtered out the literal flag string from its decrypt responses, so you couldn't just submit the flag and read it back. Block-by-block recovery worked around that filter.

## Lesson

Stateful cipher objects with reusable encrypt and decrypt are a footgun. The implementation detail that should never have leaked (the internal chaining state carried across operations) became the entire attack surface. Modern crypto libraries enforce single-direction objects exactly to avoid this.
