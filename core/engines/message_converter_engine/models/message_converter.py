from dataclasses import dataclass, asdict
from lz4.frame import compress, decompress
from numpy import uint8
from numpy.typing import NDArray
from msgpack import packb, unpackb

@dataclass
class message:
    # JWT token
    token: str
    # Message data
    data: str | NDArray[uint8]
    # Timestamp
    time: int
    # Chat ID
    chat_id: str
    # From user
    from_user: str
    # To user
    to_user: str
    # Data type
    type: int

def create_message(token: str, data: str | NDArray[uint8], time: int, chat_id: str, from_user: str, type: int, to_user: str | None = None) -> bytes:
    try:
        # Converting data
        raw_message = asdict(message(token, data, time, chat_id, from_user, to_user, type))
        # Serialization message
        packed_message = packb(raw_message)
        # Compress message
        compress_message = compress(packed_message)

        if len(compress_message) <= len(packed_message):
            return b"\x01" + compress_message
        
        return b"\x00" + packed_message
    except Exception as e:
        return f"Error: {e}"

def deserialize_message(message: bytes):
    try:
        # Remove the flag byte
        message_payload = message[1:]
        # If message is not compressed
        if message[0] == b"\x00":
            # Return deserialize message
            return unpackb(message_payload)
        # If message is compressed, it is decompressed
        decompressed_message = decompress(message_payload)
        # Return deserialize message
        return unpackb(decompressed_message)
    except Exception as e:
        return f"Error: {e}"
