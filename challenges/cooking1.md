This challenge turned out to be surprisingly simple. Initially, I spent some time figuring out how to log in as a guest to obtain a cookie. The trick was straightforward: I attempted to sign in using the username "guest," which granted me the following unencoded cookie:

```json
{ "user": "guest", "password": "123123", "admin": 0 }
```

It was in clear ASCII format with no encryption or signatures to circumvent. By simply changing the value of `admin` from `0` to `1`, I reloaded the page and found myself authenticated as an admin. Subsequently, an admin button appeared, and upon clicking it, I discovered the flag.
