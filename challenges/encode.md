In this challenge, the string didn’t appear completely random either, it consisted mostly of letters with a few special characters, like the `=` symbol at the end. This immediately raised a flag that the message might be **Base64-encoded**, since Base64 uses a predictable character set (`A–Z`, `a–z`, `0–9`, `+`, `/`) and often ends in `=` for padding to ensure the output length is a multiple of 4.

The name of the challenge, **"Encode"**, also hinted that the transformation was likely **encoding** rather than encryption. That distinction matters, encoding is typically reversible without a secret key.

The provided hint further suggested the message might be **encoded more than once**.

To test this theory, I used the following command-line pipeline to decode the string multiple times using the `base64` utility:

```bash
echo "Vmtkb2JFbEhkR3hsVTBKd1kzcHZaMDU2Vm1wWmFrVXlXVmRaZDA5RVFYaFpWRVY1V2tSak1FNUVVVEJOVjA1c1dsUk9hVmxYVFhoYWFrMDk=" | base64 -d | base64 -d | base64 -d
```

After decoding it three times, I got the final message:

```
The key is: 75cb16af0801a12d744441cee3bac1f3
```
