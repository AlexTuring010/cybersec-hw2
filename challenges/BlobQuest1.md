You thought obfuscating the source code would slow me down? I didn’t even bother trying to deobfuscate it. I just opened the console, peeked inside `game.state.states.Game`, and spotted two interesting things:

- `toggleFuncs`: an array of 12 functions
- `toggleLever`: a function

I tested those, and it was obvious — I could toggle all the buttons and flip the lever directly.

So I ran this script in the console to brute-force all combos until it clicked:

```js
const totalToggles = 12;

function tryCombo(combo) {
  // combo is a number from 0 to 4095, where each bit toggles a button
  for (let i = 0; i < totalToggles; i++) {
    if ((combo & (1 << i)) !== 0) {
      game.state.states.Game.toggleFuncs[i]();
    }
  }
  game.state.states.Game.toggleLever();
}

(async function bruteForce() {
  for (let combo = 0; combo < 1 << totalToggles; combo++) {
    tryCombo(combo);
    // Give the game 50ms to reset before next attempt
    await new Promise((r) => setTimeout(r, 50));
  }
})();
```

It’s like Blob suddenly got Jedi powers, pressing buttons with lightning speed and uncanny precision. Took a little while, sure — but with only 2¹² combos to try, it wasn’t long before I cracked it and snagged the flag.

Disclaimer: sometimes the script doesnt work, I think increasing the timeout to 100 ms may be better to avoid the glitch, give it time to process that it should show you the flag or something?

The flag is: puzzle_96c1012
