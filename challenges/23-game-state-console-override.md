# Overriding a game's death handler from the browser console

The challenge was a tiny browser game where the player ("Bob") had to reach a flag, with lasers in the way. Editing the source file in dev tools didn't update the live game, but the game state was a JavaScript object exposed on the global scope.

In the dev console:

```javascript
game.state.states.Game.onLazerHit = game.state.states.Game.playerJump;
```

Now touching a laser triggers a jump instead of dying. Bob jumps over each laser, reaches the flag area, flag prints.

## Lesson

When a frontend game exposes its state machine on the global namespace, every collision handler, score check, and win condition is monkey-patchable. The "rules" only exist if the client chooses to enforce them, and the client doesn't have to.
