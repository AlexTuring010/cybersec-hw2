This challenge provided a network capture file (`authentication.pcap`) containing a login session where the user logged in using the **flag as their password**.

The hint pointed to HTTP Basic Access Authentication, which sends credentials in the `Authorization` header, base64-encoded as `username:password`.

---

#### Step 1: Extract the HTTP Authorization header from the pcap using tshark

Using the terminal, I ran:

```bash
tshark -r authentication.pcap -Y "http.authorization" -T fields -e http.authorization
```

This displayed the line:

```
Basic am9obl9kb2U6YjA1ZDUyN2E4MTYyMzhhMWRjMjU1ZWNjMDZjYWNhMTk=
```

---

#### Step 2: Decode the Base64 string to reveal credentials

Extracting just the encoded part and decoding:

```bash
tshark -r authentication.pcap -Y "http.authorization" -T fields -e http.authorization | \
grep Basic | cut -d ' ' -f2 | base64 -d
```

Resulted in:

```
john_doe:b05d527a816238a1dc255ecc06caca19
```

---

The password part (`b05d527a816238a1dc255ecc06caca19`) is the **flag** required for the challenge.
