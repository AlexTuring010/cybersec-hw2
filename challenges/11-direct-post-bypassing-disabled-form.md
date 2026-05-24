# Bypassing UI-side form restrictions with a direct POST

A challenge form that looked simple on the surface, but the UI tried hard to stop you using it:

- The text input and submit button were both `disabled`
- Moving the mouse toward the form made it float away from the cursor

```html
<form action="/submit" method="POST">
  <input type="text" name="flag" disabled />
  <input type="hidden" name="legit" value="toteslegit" />
  <input type="submit" disabled />
</form>
```

The browser-side controls don't matter. The server still accepts a POST to `/submit`.

```javascript
fetch("/submit", {
  method: "POST",
  headers: { "Content-Type": "application/x-www-form-urlencoded" },
  body: "flag=flag&legit=toteslegit",
});
```

Simple form. Troll UX. Direct request wins.

## Lesson

Anything the browser enforces is decorative. Validation has to live on the server. Disabled attributes, hidden fields, and CSS pointer-event games stop end users; they do nothing to anyone with a console.
