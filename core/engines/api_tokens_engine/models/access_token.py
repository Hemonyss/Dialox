from dataclasses import dataclass, asdict
from secrets import token_urlsafe
import jwt
from typing import Dict, Tuple, Any
import time

@dataclass
class access_token:
    # Issuer
    iss: str
    # Subject
    sub: str
    # Audience
    aud: str
    # Expiration time
    exp: int
    # Issued at
    iat: int 
    # Access right
    right: int

def create_access_token(iss: str, sub: str, aud: str, right: int, exp: int = int(time.time()) + 900, iat: int = int(time.time())) -> Tuple[str | bytes, str]:
    # Transforming dataclass to dict
    access_token_dict = asdict(access_token(iss, sub, aud, exp, iat, right))
    # Generate 256 bit key
    encode_key = token_urlsafe(32)
    # Encode token
    access_token_encode = jwt.encode(payload=access_token_dict, key=encode_key, algorithm="HS256")

    return (encode_key, access_token_encode)

def decode_access_token(token: str | bytes, key: str, aud: str) -> Dict[str, Any]:
    try:
        # Decode token
        payload = jwt.decode(
            token,
            key,
            algorithms="HS256",
            options={"verify_exp": True, "verify_iat": True},
            audience=aud,
            leeway=30
        )
        # Verification that the token was created by the sender
        if payload["iss"] != payload["sub"]:
            raise jwt.InvalidTokenError("Iss and sub not equal")

        if payload["sub"] == payload["aud"]:
            raise jwt.InvalidTokenError("sub and aud equal")

        return payload
    except jwt.ExpiredSignatureError:
        return "The token is expired"
    except jwt.InvalidSignatureError:
        return "Incorrect signature"
    except jwt.InvalidTokenError as e:
        return f"Invalid token: {e}"
t = create_access_token("1", "1", "2", 1)
