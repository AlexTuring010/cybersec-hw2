# Spotting an Atbash cipher under frequency analysis

The given block of text had English-looking structure (punctuation, spaces) but the words were nonsense. Standard first move: try frequency analysis to identify a substitution cipher.

I matched a few common letters (`e → v`, `g → t`) and noticed the recurring word `gsv`. With my guesses, that mapped to `tse`, not a word. But if `t` and `e` were right and `s → h`, it became `the`. That fit.

I could've kept going letter by letter, but the challenge's name and hint were doing some heavy lifting: the title reversed spelled "Atbash". The Atbash cipher flips the alphabet (`A ↔ Z`, `B ↔ Y`, …). Running the ciphertext through Atbash decoded cleanly:

> "Although the Atbash cipher can be solved as a cryptogram, it actually pre-dates many other systems..."

## Lesson

Read the title, read the hint, then start crunching. The setter is talking to you, and "ten seconds re-reading the prompt" beats "thirty minutes of analysis" most of the time.
