import logging
import hashlib
import hmac

class EAPOLMessage:
    """Simplified EAPOL-Key structure for KRACK simulation"""
    def __init__(self, 
                 replay_counter: int = 0,
                 key_nonce: bytes = None):
        self.replay_counter = replay_counter
        self.key_nonce = key_nonce or b'\x00'*32

    def serialize(self) -> bytes:
        """Serialize to bytes"""
        serialized =  b''.join([
            self.replay_counter.to_bytes(8, 'big'),
            self.key_nonce
        ])

        return serialized
    
    @classmethod
    def deserialize(cls, data):
        """Deserialize from bytes"""
        if len(data) < 40:  # 8 + 32 = 40 bytes 
            raise ValueError(f"Invalid EAPOL length: {len(data)} < 40")
        
        return cls(
                replay_counter=int.from_bytes(data[:8], 'big'),
                key_nonce=data[8:]
        )
        
    def __str__(self):
        return (f"EAPOL[rc={self.replay_counter}, "
                f"nonce={self.key_nonce.hex()}]")

