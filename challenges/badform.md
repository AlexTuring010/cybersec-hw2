This challenge presented a form that looked simple on the surface, but was intentionally made difficult to interact with through the UI. The hint said:

> “Just enter 'flag' and this site will give you one. What could be simpler?”

However, the form had some deliberate obstacles:

```html
<form action="/submit" id="daform" method="POST">
  <input type="text" name="flag" value="trololol" disabled="" />
  <input type="hidden" name="legit" value="toteslegit" />
  <input type="submit" value="submit" disabled="" />
</form>
```

- The `flag` input and submit button were both `disabled`.
- Moving the mouse toward the form made it float away, preventing interaction.

Rather than fighting with the UI, I bypassed it entirely by using a `fetch` request directly from the browser console:

```javascript
fetch("/submit", {
  method: "POST",
  headers: {
    "Content-Type": "application/x-www-form-urlencoded",
  },
  body: "flag=flag&legit=toteslegit",
})
  .then((res) => res.text())
  .then((text) => console.log(text));
```

This manually replicated the form submission with the correct values, avoiding the disabled fields and any JavaScript trickery.

The server responded with the flag:

```
How did you get my flag?!? no_form_can_stop_me_2a6345a6e36af4934363332d3ef992db
```

Simple form. Troll UX. Direct request wins.
