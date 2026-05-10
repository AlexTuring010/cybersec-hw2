This challenge wasted _way_ more of my time than it should have.

## Phase 1: The Descent Into Madness

- **First Theory (Schizo Mode):**  
  I became convinced there were hidden letters in the spectrogram. Spent _hours_ tweaking audio settings, trying to "clear it up" to reveal secret messages. (Spoiler: There were none.)

- **LSB Steganography Attempt:**  
  Wrote a Python script to check least significant bits in the file. Nothing.

- **Tool Overload:**  
  Downloaded every stego tool I could find online, still no progress.

- **Original Audio Comparison:**  
  Found the source audio and compared it to the challenge file. At least this confirmed the "letters" I saw in the spectrogram were just part of the original.

## Phase 2: The Breakthrough

- **Brute-Force Savior (`stegseek`):**  
   Finally tried brute-forcing `steghide` with `stegseek` using `rockyou.txt`.  
  Extracted rocket blueprints (a JPG file).

- **Second Round of `stegseek`:**  
  Ran it again on the rocket image. Got a text file:
  ```
  seeing_whats_truly_sent_is_hard!
  ```
  No hidden data this time, just raw data in ASCII form.

## Phase 3: The Final Troll

- **Flag? Where?**  
  Tried submitting the text as the flag. Failed.  
  **Mistake:** I omitted the exclamation mark (thought it was just emphasis).

- **Spiral of Doubt:**  
  Convinced myself it was a dead end. Went back to analyzing the audio/image _again_.

- **Redemption:**  
  Hours later, re-submitted the text _with_ the exclamation mark.  
  **Flag accepted.** 80 points earned at the cost of my sanity.

Final Thought:  
`seeing_whats_truly_sent_is_hard!` — indeed it is.
