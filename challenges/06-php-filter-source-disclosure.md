# Leaking PHP source through the filter wrapper

A web challenge with a broken number-guess game (always wrong, even on the right number). The hint mentioned the page parameter.

The site used `nav.php?page=<name>` to load sections, building file paths from the parameter without validation. PHP's stream wrapper system lets you read source files through a base64 filter:

```
nav.php?page=php://filter/convert.base64-encode/resource=<target>
```

The page rendered the base64 encoding of the target file's source. Decoding revealed the actual game logic, including how the flag was generated.

## Lesson

Any unvalidated input that becomes part of a file path or `include()` argument is a candidate for source disclosure. PHP's wrapper system makes this trivial when the parameter feeds an `include`, `require`, or `file_get_contents` call. The `php://filter` wrapper exists for the same reasons it makes this attack work.
