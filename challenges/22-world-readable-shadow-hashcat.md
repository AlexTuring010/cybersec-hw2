# World-readable /etc/shadow to root

I logged in over SSH as an unprivileged `agent` user with credentials the challenge handed me. Standard shell, nothing exciting. The directory holding the flag was owned by another user with no read access for me.

About to start looking at running processes when I glanced at `/etc/shadow`:

```bash
$ ls -la /etc/shadow
-rw-r--r-- 1 root shadow 819 May 19 20:56 /etc/shadow
```

World-readable. That's all it took.

```
secret:$5$<salt>$<hash>:...
```

`$5$` is SHA-256 crypt, the modern `/etc/shadow` format. Hashcat mode 7400 plus rockyou:

```bash
hashcat -m 7400 shadow.txt rockyou.txt
```

A few hundred thousand guesses in, the password came back as a common dictionary word. `su secret`, walk into the protected directory, read the flag.

## Lesson

Shadow file permissions matter. A `-r--r--r--` shadow turns offline cracking from a privileged operation into a `chmod` problem. The point of separating `/etc/passwd` and `/etc/shadow` is precisely to keep hashes out of unprivileged hands; once that boundary breaks, every weak password on the box is a stepping stone.
