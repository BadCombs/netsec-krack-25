import hashlib
import hmac
import pyfiglet

SERVER_ADDR = "localhost"
SERVER_PORT = 1234
MITM_ADDR = "localhost"
MITM_PORT = 5678
BUFF_SIZE = 512
DELAY = 1

# MAC addresses
CLIENT_MAC = "aa:bb:cc:dd:ee:ff"
AP_MAC = "11:22:33:44:55:66"

# Cryptographic parameters
PMK = "PairwiseMasterKey1234567890!"  # In real WPA2, this comes from PBKDF2
KCK_LENGTH = 16  
KEK_LENGTH = 16
TK_LENGTH = 16 

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_splash_screen(s :str) -> str:
    return str(pyfiglet.figlet_format(s, font="3-d"))

def calculate_ptk(anonce, snonce):
    """ 
        Simulate PTK calculation
        Real:     PTK = PBKDF2(PMK, "Pairwise key expansion", 
                   min(AP_MAC, CLIENT_MAC) + max(AP_MAC, CLIENT_MAC) +
                   min(ANonce, SNonce) + max(ANonce, SNonce))
    """
    ptk_input = f"{PMK}{AP_MAC}{CLIENT_MAC}{anonce.hex()}{snonce.hex()}".encode()
    ptk = hashlib.sha256(ptk_input).digest()
    
    # Split into components 
    kck = ptk[:KCK_LENGTH]
    kek = ptk[KCK_LENGTH:KCK_LENGTH+KEK_LENGTH]
    tk  = ptk[KCK_LENGTH+KEK_LENGTH:KCK_LENGTH+KEK_LENGTH+TK_LENGTH]
    
    return {
        'kck': kck, # KeyConfirmationKey
        'kek': kek, # Key Encryption Key
        'tk': tk, # Temporal Key
        'full': ptk
    }

