from dataclasses import dataclass, asdict
from secrets import token_urlsafe
import jwt
from typing import Dict, Any
import time

@dataclass
class access_token:
    # Sender ID
    sen_id: int
    # Recipient ID
    rec_id: int
    # Expiration time
    exp: int
    # Creation time
    iat: int 
    # Access right
    right: int

def create_access_token(sen_id: int, rec_id: int, right: int, exp: int = int(time.time()) + 900, tac: int = int(time.time())) -> Dict[str, Any]:
    access_token_dict = asdict(access_token(sen_id, rec_id, exp, tac, right))
    encode_key = token_urlsafe(32)

    access_token_encode = jwt.encode(access_token_dict, encode_key, algorithm="HS256")

    return (encode_key, access_token_encode)
