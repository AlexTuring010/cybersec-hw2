# Blind SQLi through an unexpected parameter

A social-network-style site with aggressive filtering on the visible login form ("NO HACKING ALLOWED!!" returned for anything non-alphanumeric, no spaces, etc.). Spent a long time trying to attack the form before realizing the *real* injection point was somewhere else.

## The actual attack surface

After logging in as a normal user and looking at the page source, the "like" button fired this:

```html
<script>
$('.facebutton').click(function() {
  $.ajax({
    type:'POST',
    url:'/face',
    data: "id=" + $(this).attr('id').substring(1) + "&csrf=<token>",
  });
});
</script>
```

That `id` parameter wasn't being filtered the way the login form was. A single quote on `id` returned a 500. SQL injection confirmed, but blind: no echoed output.

## Blind SQLi via boolean responses

Two distinct server responses gave a true/false oracle:

- Valid query: `{"success": false}` (you already liked it)
- Invalid query: a red "STOP TRYING TO HACK US" page

So queries like `1' AND (SELECT LENGTH(password) FROM users WHERE name='admin') < N--` could be tested for true vs false by inspecting the response.

## Recovery loop

Standard blind SQLi: scan one character at a time using `SUBSTR(password, pos, 1) = 'X'`. Pseudocode:

```text
for pos = 1 to known_length:
    for ch in charset:
        if oracle("1' AND SUBSTR(password,pos,1)='" + ch + "'--"):
            password += ch
            break
```

A few quirks to handle:

- CSRF tokens expire. The loop needs to refresh on stale-token errors.
- The "STOP TRYING TO HACK US" page also fires on expired CSRF, so a stuck position usually means "refresh token" rather than "wrong charset".

I wrapped this in a small browser-console UI with a resume-from-partial feature, because watching paint dry without a progress bar is bleak.

## Lesson

When a form is filtered hard, look for *every* place the user can influence a query. Visible inputs are the obvious attack surface; AJAX endpoints, hidden fields, and IDs in `data-*` attributes often aren't sanitized the same way.
