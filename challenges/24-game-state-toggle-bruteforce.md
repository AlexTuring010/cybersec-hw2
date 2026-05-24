# Brute-forcing a 12-toggle puzzle through the game state

A "sequel" browser-game challenge, this one with obfuscated source code. I didn't bother deobfuscating. The live `game.state` object exposed:

- `toggleFuncs`: an array of 12 toggle functions
- `toggleLever`: a function that checks the combination

12 toggles = 4096 combinations. Cheap to brute-force from the console:

```javascript
const N = 12;

function applyCombo(combo) {
  for (let i = 0; i < N; i++) {
    if (combo & (1 << i)) game.state.states.Game.toggleFuncs[i]();
  }
  game.state.states.Game.toggleLever();
}

(async () => {
  for (let combo = 0; combo < 1 << N; combo++) {
    applyCombo(combo);
    await new Promise(r => setTimeout(r, 50));
  }
})();
```

The 50ms delay lets the game reset between tries; tighter values race the game loop and miss the success state.

## Lesson

Obfuscating client-side code does nothing if the game state is still exposed on the window object. Whatever functions are reachable, an attacker can call directly, and a 4096-element search space falls in seconds.
