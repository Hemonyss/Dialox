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
    type: int # 0 - perfectly compressible data (message, txt and other); 1 - image; 2 - audio; 3 - already compressed data (zip, 7z, rar and other archive)

def create_message(token: str, data: str | NDArray[uint8], time: int, chat_id: str, from_user: str, type: int, to_user: str | None = None) -> bytes:
    try:
        # Converting data
        raw_message = asdict(message(token, data, time, chat_id, from_user, to_user, type))
        # Message data type
        data_type = raw_message['type']
        # Default serialization message
        packed_message = packb(raw_message)
        
        # How to compress
        if data_type == 0:
            # Serialization message
            packed_message = packb(raw_message)
            # Compress message
            output = lz4_compress(packed_message)
        elif data_type == 1:
            # Import image compressor
            from ..io.read.image_compress import image_compress
            # Compress image
            compress_image = image_compress(image_path=raw_message['data'])
            # Adding a compressed image to a message
            raw_message['data'] = compress_image.tobytes()
            # Serialization message
            output = packb(raw_message)

            return output
        elif data_type in [2, 3]:
            packed_message = packb(raw_message)

        if data_type != 3 and len(output) <= len(packed_message):
            return data_type.to_bytes(1, 'little') + output
        
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

def lz4_compress(data: bytes) -> bytes:
    return compress(data)
