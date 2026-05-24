# Flipping an admin bit in an unsigned cookie

The site issued a guest session cookie like:

```json
{"user": "guest", "password": "123123", "admin": 0}
```

Plain JSON, no encryption, no signature. Flip `admin` to `1`, send the modified cookie, refresh. Admin button appears, flag is behind it.

## Lesson

Cookies the server trusts need to be signed (or stored server-side and referenced by an opaque session ID). Anything else is "the client is the database".
