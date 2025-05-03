import os
import logging
import socket
from time import sleep
from const import *

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def step_prompt(description):
    input(f"{Colors.YELLOW}[Press Enter to {description}]{Colors.END}")

def log_phase(phase_num, description):
    logging.info(f"\n{Colors.HEADER}=== PHASE {phase_num}: {description} ==={Colors.END}\n")

def setup_logging():
    logging.basicConfig(
        format=f"{Colors.BLUE}[%(asctime)s]{Colors.END} %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO
    )

def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

def connect_with_retry(sock, addr, port, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            sock.connect((addr, port))
            return True
        except ConnectionRefusedError:
            sleep(DELAY)
            retries += 1
    return False

def xor_cipher(data: bytes, key: bytes) -> bytes:
    """Simple repeating-key XOR (for demo only)."""
    return bytes(b ^ key[i % len(key)] for i,b in enumerate(data))

