# HTTP Basic Auth credentials from a pcap

A network capture recorded a login session where the user logged in with the flag as their password. The hint pointed at HTTP Basic Access Authentication, which carries credentials in the `Authorization` header as `base64(username:password)`, plaintext over the wire.

## Extract the header with tshark

```bash
tshark -r capture.pcap -Y "http.authorization" -T fields -e http.authorization
```

Returns a single line: `Basic <base64-blob>`.

## Decode

```bash
tshark -r capture.pcap -Y "http.authorization" -T fields -e http.authorization \
  | grep Basic | cut -d ' ' -f2 | base64 -d
```

Out drops `username:password`, where the password half is the flag.

## Lesson

HTTP Basic Auth over an unencrypted channel is a sieve. The base64 encoding is not encryption; it's just framing. If you ever see Basic Auth in a real capture, the credentials are already gone.
