# When you are too bored to try at max 16 possible values to find the offset manually
# and you instead write a whole script for that, thats why good programmers must be lazy

import socket

def connect_to_service(agent_number):
    # Connect to the remote service
    host = "shell.hackintro25.di.uoa.gr"
    port = 65095

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Read the banner
        banner = s.recv(4096).decode()
        print(banner)

        # Send the agent number
        s.sendall(f"{agent_number}\n".encode())

        # Receive the ciphertext
        ciphertext = s.recv(4096).decode().strip()
        return ciphertext

def find_offset():
    previous_length = 0
    for i in range(1, 50):  # Try agent numbers of increasing length
        agent_number = "1" * i
        print(f"Trying agent number: {agent_number}")

        # Get the ciphertext
        ciphertext = connect_to_service(agent_number)
        print(f"Ciphertext: {ciphertext}")

        # Check the length of the ciphertext
        current_length = len(ciphertext)
        print(f"Ciphertext length: {current_length}")

        # If the length increases, we've crossed a block boundary
        if previous_length and current_length > previous_length:
            print(f"Block boundary crossed at agent number length: {i}")
            print(f"Offset length: {previous_length - 160} bytes")
            break

        previous_length = current_length

if __name__ == "__main__":
    find_offset()