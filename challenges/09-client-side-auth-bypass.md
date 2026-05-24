# "Auth" implemented entirely in client-side JavaScript

The login page hashed the input password in JavaScript and compared the digest to a hard-coded value:

```javascript
function login() {
  const hash = sjcl.hash.sha256.hash(document.getElementById("password").value);
  const digest = sjcl.codec.hex.fromBits(hash);
  if (digest === "<hard-coded sha256>") {
    document.location = "./<random-looking>.html";
  } else {
    alert("Incorrect password!");
  }
}
```

The "protected" page's URL is literally in the source. No cracking needed. Append the path to the site root and visit it directly. Flag was on that page.

## Lesson

Nothing the client knows is a secret from the client. Validation needs a server. A SHA-256 compared in JavaScript is theater.
