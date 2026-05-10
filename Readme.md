**Name:** Αλέξανδρος Γκιάφης  
**SDI:** 2200284  
**HackCenter Username:** alexturing

In this assignment, I solved **all challenges**, securing **3rd place on the leaderboard**. My success wasn’t about technical skill, it came from **resilience**. When I hit dead ends, I didn’t give up. I experimented and found solutions.

I’ve written detailed write-ups for **every challenge** (not just the required one) inside the challenges directory. I also got a lot of scripts I used throughout the days in the scripts directory (its a bit of a mess). If I had to pick my favorite challenges, here they are:

### **1. The Facebook 1**

This challenge made me feel like a **real hacker**. Most people interact with forms through the website interface, but I dug deeper—**injecting into the like button ID**. I even built a **cool console tool** with a mini UI that **generates a target’s password one letter at a time** using **blind sql injection**. It wasn’t obvious, and that’s what made it rewarding.

### **2. Cloudz**

Having the **source code** was a game-changer—no more blind attacks! The solution had **three key steps**:

1. **SQL injection** to leak a hash via error messages.
2. **Cracking the hash**, not to log in, but to
3. **forge an admin cookie**.

The real trick? The server **only checked the last character** of the signature. No brute-forcing the whole thing—just **one character**.

### **3. BrokenEncryption0 (Crypto)**

This one was all about **understanding ECB mode**. Since identical plaintext blocks encrypt to identical ciphertexts, I **brute-forced the flag letter by letter** with a precise script. (explaining it more in challenge writeup)

### **4. tworc2 (Crypto)**

Not the hardest, but **satisfying**. Normally, the python library doesnt allow the same cryptor to both encrypt and decrypt right after. But this one is another version? Once I figured out how the cryptor in the script worked, I crafted a smart plan to **decrypt the flag in blocks**.

### Honorable Mention: The Facebook 2

It had the **most points**, but honestly, once I found the **injection point (error page)**, it only took **two payloads** to get the flag. The reason more people didn’t solve it? They gave up too soon—**they didn’t explore enough**.
