**12:06 PM.**

_Cynaegeirus_ had left for lunch — as he always does — with the consistency of a man who thinks **routine is a substitute for operational security**.

He is wrong.

---

I logged into his machine using the credentials provided:

```bash
ssh agent@shell.hackintro25.di.uoa.gr -p 28325
Password: toastY
```

Standard unprivileged shell. Nothing I hadn’t seen before.
Nothing worth raising an eyebrow over — let alone an alert.

---

I checked `/secrets` first. Of course.

```bash
drwxr-x--- 2 secret secret 4096 May 19 20:56 /secrets
```

- **Owner:** secret
- **Group:** secret
- **Permissions:** not mine.

I’ve always liked the name **"secret"** — it carries a certain irony when attached to users this careless.

---

I was about to do a basic sweep of running processes when I happened to glance at `/etc/shadow`.
Not because I expected much — just instinct. Like checking both ways before jaywalking across an encrypted highway.

And yet:

```bash
-rw-r--r-- 1 root shadow 819 May 19 20:56 /etc/shadow
```

**Readable.** World-readable, in fact.

Apparently, Cynaegeirus believes in _open access._
At least when it comes to **critical system files**.

---

Inside the file, this caught my attention:

```bash
secret:$5$rr/98tD56y3UdDkh$gXF58mvsoSv48XvBQruwLVKxGnPRiK9fDrC2dl5LZ32:...
```

- **SHA-256 crypt.**
  Not the worst choice. But it’s not about the hash — it’s about the password behind it.
  And people? People are predictable.

---

Back on my machine, I saved the hash into `shadow.txt` and launched the attack:

```bash
hashcat -m 7400 shadow.txt rockyou.txt
```

> (Yes, `-m 7400`. That tells hashcat it’s dealing with SHA-256 crypt — the format used by modern `/etc/shadow` entries)

A few hundred thousand guesses later — `rockyou.txt` doing what `rockyou.txt` was born to do — the password emerged:

```bash
studio
```

_Of course it was._

---

I returned to the shell, no rush:

```bash
$ su secret
Password: studio
```

A heartbeat. Then **access**.

Inside `/secrets`, the flag was waiting — unguarded, unbothered.

```bash
$ cat /secrets/flag.txt
```

There it was.
**Simple. Elegant. Utterly unsecured.**

---

I took another sip of mint tea.
Still warm. **Perfect.**

The machine would format itself by tomorrow, wiping the logs clean, resetting the system, erasing every trace —
**except, of course, the one that mattered.**

---

> _I don’t leave fingerprints._ > **But I do leave echoes.**

<br>

<div align="right">

**— Agent X** ☕💻
_Access granted. Tea infused. Secrets retrieved._

</div>
