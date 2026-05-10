This was a web challenge where we had to "guess" a number between 1 and 10, but something was broken - even when entering the correct number, it always said the guess was wrong. The hint suggested looking at the page parameter, so I started playing around with the URL.

I noticed the site was using nav.php with a page parameter to load different sections. Remembering the hint, I tried to leak the source code by using a PHP filter wrapper. I entered this URL:

http://shell.hackintro25.di.uoa.gr:5156/nav.php?page=php://filter/convert.base64-encode/resource=guess

This returned a big block of base64 encoded text. After decoding it, I could see the actual PHP code behind the guessing game. The code revealed the flag
