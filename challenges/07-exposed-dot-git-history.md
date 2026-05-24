# Recovering a deleted file from an exposed .git directory

A web app shipped with the `.git` directory inside the webroot. The hint mentioned reverting a "bad commit". That's a dot-git directory waiting to be dumped.

```bash
gitdumper.sh http://<host>/.git/ ./repo
cd repo
git log --oneline
```

Two commits showed up. The latest was a "typo fix" that had removed the flag file; the previous commit was a real commit titled like an actual feature.

```bash
git checkout <earlier-commit>
cat flag.txt
```

There it was.

## Lesson

`.git` exposure is one of the most common deployment mistakes. Anything that's ever been committed to the repository (secrets, removed files, debug code) is recoverable. Always serve from a build artifact directory, or block `.git/` at the web server level.
