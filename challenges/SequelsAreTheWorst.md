This was a classic SQL injection challenge, simple but effective. I'm no SQL expert and haven't written a query in over a year, but I had a hunch that the backend was executing something like this:

```sql
SELECT * FROM users WHERE username = '<username>' AND password = '<password>';
```

To bypass this kind of login check, a common SQL injection technique is to input:

- **Username**: `admin' --`
- **Password**: _(leave blank or enter anything)_

This manipulates the query to become:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = '';
```

Here’s what’s happening:

- `'admin'` is the target username.
- `--` is the SQL comment syntax, which tells the database to ignore the rest of the line.
- As a result, the password condition is completely skipped.

The final effect? The system only checks whether the username is `'admin'`, and if that user exists, it logs you in—**no password verification required**.

And yes, I tried it, and it worked.
