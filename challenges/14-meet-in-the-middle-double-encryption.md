# Meet-in-the-middle on a 2DES-style construction

The encryption was a two-layer block cipher with short keys (3 bytes each, zero-padded to 5):

```python
ct = cipher2.encrypt(cipher1.encrypt(plaintext))
```

So `ct = E_{k2}(E_{k1}(pt))`.

Brute-forcing both keys naively means `2^24 × 2^24 = 2^48` work, impractical on a laptop. But because the two layers are independent, there's a meet-in-the-middle attack that cuts it to `2^25`.

## The MITM attack

Given a known plaintext/ciphertext pair `(pt, ct)`:

1. For every candidate `k1` (`2^24` values), encrypt `pt` and store `(E_{k1}(pt), k1)` in a hash map keyed on the intermediate value.
2. For every candidate `k2` (`2^24` values), decrypt `ct`: compute `D_{k2}(ct)` and look it up in the map.
3. A hit means `E_{k1}(pt) = D_{k2}(ct)`, i.e. you've found the `(k1, k2)` pair the server is using.

Total cost: `2^24 + 2^24` time, `2^24` memory. Runs in under an hour on a laptop without optimization.

With both keys recovered, decrypt the actual flag ciphertext the same way.

## Lesson

Doubling a cipher doesn't double the keyspace. Given known plaintext, MITM brings double encryption back down to roughly single-cipher complexity (in time, at the cost of memory). This is exactly why 3DES uses *three* keys instead of two; the third layer pushes the time/memory tradeoff out of reach.
