from collections import Counter
import string

with open("BashAt.txt", "r") as file:
    text = file.read()

filtered_text = [char.upper() for char in text if char.isalpha()]

letter_counts = Counter(filtered_text)

sorted_counts = sorted(letter_counts.items(), key=lambda x: x[1], reverse=True)

for letter, count in sorted_counts:
    print(f"{letter}: {count}")
