# My masterpiece attack script that brute forces the flag characters one character at a time!

import socket
import string
from tqdm import tqdm  # not necessary but I like seeing the loading bar while waiting

# Configuration
HOST = "shell.hackintro25.di.uoa.gr"
PORT = 65095
BLOCK_SIZE = 16  # AES block size in bytes
FLAG_LENGTH = 49  # Length of the flag to recover
CHARSET = string.printable  # Characters to brute force (printable ASCII)

def connect_to_service(agent_input):
    """Connect to the service and send the agent input."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Read the banner
        s.recv(4096).decode()

        # Send the agent input
        s.sendall(f"{agent_input}\n".encode())

        # Receive the ciphertext
        ciphertext = s.recv(4096).decode().strip()
        return ciphertext

# Padding to ensure the correct block length
def pad(message: str) -> bytes:
    padded = message + '1'
    while len(padded) % 16 != 0:
        padded += '0'
    return padded

def brute_force_flag():
    """Recover the flag byte by byte."""
    recovered_flag = ""

    for i in range(FLAG_LENGTH):
        print(f"Recovering character {FLAG_LENGTH - i}...")

        agent_padding = "A" * 10  # Reserve 10 characters for the first block
        agent_offset = "B" * (i + 2)  # Offset the flag by i characters
        
        flag = "?" * (FLAG_LENGTH - i) + recovered_flag

        input = "?" + recovered_flag
        if len(input) >= 16:
            input = input[:16]
            input = agent_padding + input + agent_offset
        else: 
            input = agent_padding + pad(input) + agent_offset
        
        plain_text = f"agent {input} wants to see {flag}"
        print(f"{pad(plain_text)}")
    
        # Brute force the current character
        found = False
        char = ""
        for char in tqdm(CHARSET, desc="Brute-forcing character", ncols=80):
            # Construct the agent input for brute forcing
            input = char + recovered_flag
            if len(input) >= 16:
                input = input[:16]
                input = agent_padding + input + agent_offset
            else:
                input = agent_padding + pad(input) + agent_offset

            ciphertext = connect_to_service(input)
            seventh_block = ciphertext[(7 - 1) * BLOCK_SIZE * 2 : 7 * BLOCK_SIZE * 2]
            second_block = ciphertext[BLOCK_SIZE * 2:BLOCK_SIZE * 4]

            # Check if the blocks match
            if seventh_block == second_block:
                recovered_flag = char + recovered_flag
                found = True
                break
        
        # If no character was found, print a fail message
        if not found:
            print(f"Failed to recover character {FLAG_LENGTH - i}.")
            break
        else:
            print(f"Found character: {char}")

    return recovered_flag

if __name__ == "__main__":
    flag = brute_force_flag()
    print(f"Recovered flag: {flag}")