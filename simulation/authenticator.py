import socket
import logging
from eapol import EAPOLMessage
from const import *
from utils import *

class WiFiAP:
    def __init__(self):
        self.ptk = None
        self.anonce = hashlib.sha256(b"APNonce").digest()
        self.snonce = None
        self.replay_counter = 0
        self.socket = None

    def start(self) -> None:
        logging.debug("Initialization server socket")
        self.socket = create_socket()
        self.socket.bind((SERVER_ADDR, SERVER_PORT))
        self.socket.listen(1)

    def create_msg1(self) -> bytes:
        """Create Message 1 of 4-way handshake"""
        return EAPOLMessage(
            replay_counter=self.replay_counter,
            key_nonce=self.anonce,
        ).serialize()

    def process_msg2(self, eapol_msg) -> None:
        """Process Message 2 of 4-way handshake"""
        self.snonce = eapol_msg.key_nonce
        logging.info(f"Received SNonce: ...{self.snonce.hex()[-8:]}")

        # Calculate PTK
        self.ptk = calculate_ptk(
            self.anonce, # raw 32-byte
            self.snonce # raw 32-byte
        )
        logging.info(f"Calculating PTK...")
        logging.info(f"Installed PTK: {self.ptk['full'].hex()}")

    def create_msg3(self):
        """Create Message 3 of 4-way handshake"""
        msg = EAPOLMessage(
            replay_counter=self.replay_counter + 1
        )

        return msg.serialize()

    def run_handshake(self, conn) -> bool:
        log_phase(1, "Initial 4-way Handshake")
        
        try:
            # Send Msg1
            step_prompt("send Msg1 (ANonce)")
            msg1 = self.create_msg1()
            conn.send(msg1)
            logging.info(f"Sent Msg1: {EAPOLMessage.deserialize(msg1)}")

            # Wait for Msg2
            data = conn.recv(BUFF_SIZE)
            msg2 = EAPOLMessage.deserialize(data)
            logging.info(f"Received Msg2: {msg2}")
            self.process_msg2(msg2)    

            # Send Msg3
            step_prompt("send Msg3 (without GTK)")
            msg3 = self.create_msg3()
            conn.send(msg3)
            logging.info(f"Sent Msg3: {EAPOLMessage.deserialize(msg3)}")

            # Wait for Msg4 (but don’t block forever)
            step_prompt("wait for Msg4. Socktime out started!")
            conn.settimeout(5.0)
            
            data = conn.recv(BUFF_SIZE)
            msg4 = EAPOLMessage.deserialize(data)
            logging.info(f"Received Msg4: {msg4}")
        except socket.timeout:
            logging.warning("No Msg4 received (timeout), retransmitting Msg3...")
            return False
        except Exception as e:
            logging.error(f"Handshake error: {str(e)}", exc_info=True)
            return False

        logging.info("Handshake complete!")
        return True

    def retransmit_msg3(self, conn):
        """Retransmit same Message 3"""
        log_phase(3, "Retransmitting Msg3")

        msg = EAPOLMessage(
            replay_counter=self.replay_counter + 1,  # reuse original
        ).serialize()

        conn.send(msg)
        logging.info(f"Retransmitted Msg3: {EAPOLMessage.deserialize(msg)}")
           
    def run(self):
        clear_screen()
        print(Colors.YELLOW, print_splash_screen("AP"), Colors.END)
        setup_logging()
        self.start()
        
        logging.info("Waiting for MITM connection...")
        conn, addr = self.socket.accept()
        logging.info(f"Connected to {addr[0]}")
        
        try:
            success = self.run_handshake(conn)
            if not success:
                # Timed out, resend msg3
                self.retransmit_msg3(conn)
                logging.info("=== HANDSHAKE COMPLETE ===")
        finally:
            conn.close()
            input("\nPress Enter to exit...")

if __name__ == "__main__":
    ap = WiFiAP()
    ap.run()

