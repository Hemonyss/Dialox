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
    # Converting data
    raw_message = f"{token}.{time}.{chat_id}.{from_user}.{to_user}.{type}.{data}"
    # Converting message to bytes
    byte_message = raw_message.encode("utf-8")
    # Compress message
    compress_message = compress(byte_message)

    return compress_message if len(compress_message) < len(byte_message) else byte_message
