import socket
import logging
from eapol import *
from const import *
from utils import *

class WiFiClient:
    def __init__(self):
        self.ptk = None
        self.anonce = None
        self.snonce = hashlib.sha256(b"ClientNonce").digest()
        self.replay_counter : int = 0
        self.socket = None

    def connect_to_mitm(self) -> bool:
        self.socket = create_socket()
        if not connect_with_retry(self.socket, MITM_ADDR, MITM_PORT):
            logging.error("Failed to connect to MITM")
            return False
        return True

    def process_msg1(self, eapol_msg) -> None:
        """Process Message 1 of 4-way handshake"""
        self.anonce = eapol_msg.key_nonce
        logging.info(f"Received ANonce: ...{self.anonce.hex()[-8:]}")
        # Calculate PTK
        self.ptk = calculate_ptk(
            self.anonce, # raw 32-byte
            self.snonce # raw 32-byte
        )
        logging.info(f"Calculating PTK...")

    def create_msg2(self) -> bytes:
        """Create Message 2 of 4-way handshake"""
        msg = EAPOLMessage(
            replay_counter=self.replay_counter,
            key_nonce=self.snonce
        )
        logging.info(f"Sending SNonce: {self.snonce.hex()}")
        return msg.serialize()

    def create_msg4(self) -> bytes:
        """Create Message 4 of 4-way handshake"""
        return EAPOLMessage(
            replay_counter=self.replay_counter + 2,
        ).serialize()

    def run_handshake(self) -> bool:
        log_phase(1, "Initial 4-way Handshake")
        
        try:
            # Receive Msg1
            data = self.socket.recv(BUFF_SIZE)
            
            msg1 = EAPOLMessage.deserialize(data)
            logging.info(f"Received Msg1: {msg1}")
            self.process_msg1(msg1)

            # Send Msg2
            step_prompt("send Msg2 (SNonce)")
            msg2 = self.create_msg2()
            self.socket.send(msg2)
            logging.info(f"Sent Msg2: {EAPOLMessage.deserialize(msg2)}")

            # Receive Msg3
            data = self.socket.recv(BUFF_SIZE)
            msg3 = EAPOLMessage.deserialize(data)
            logging.info(f"Received Msg3 (confirmation): {msg3}")
            logging.info(f"Installed PTK: {self.ptk['full'].hex()}")

            # Send Msg4
            step_prompt("send Msg4 (Confirmation)")
            msg4 = self.create_msg4()
            self.socket.send(msg4)
            logging.info(f"Sent Msg4: {EAPOLMessage.deserialize(msg4)}")

            return True

        except Exception as e:
            logging.error(f"Handshake error: {str(e)}", exc_info=True)
            return False
 
    def reinstall_keys(self) -> None:
        # Receive the retransmitted Msg3 as EAPOL
        data = self.socket.recv(BUFF_SIZE)
        msg3_retx = EAPOLMessage.deserialize(data)
        logging.info(f"Received retransmitted Msg3: {msg3_retx}")
        # Simulate reinstallation
        print(Colors.RED, f"Re-installed SAME PTK!", Colors.END)
        step_prompt("send Msg4 (retransmit)")
        msg4 = self.create_msg4()
        self.socket.send(msg4)
        logging.info(f"Sent Msg4 (retransmit): {EAPOLMessage.deserialize(msg4)}")

    def run(self) -> None:
        clear_screen()
        print(Colors.GREEN, SUPPLICANT_SLPASH_SCREEN, Colors.END)
        setup_logging()
        
        if not self.connect_to_mitm():
            logging.info("Failed to connect to the MitM (client)")
            return

        try:
            initial = self.run_handshake()
            if initial:
                self.reinstall_keys()
                print(Colors.CYAN, f"===HANDSHAKE FINISHED===", Colors.END)
        finally:
            self.socket.close()
            input("\nPress Enter to exit...")

if __name__ == "__main__":
    client = WiFiClient()
    client.run()

