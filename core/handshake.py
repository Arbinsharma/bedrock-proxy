import json
import base64

def b64url_decode(s: str) -> bytes:
    s = s + "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

def b64url_encode(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()

def parse_jwt_chain(jwt_chain: str):
    parts = jwt_chain.split(".")
    return [json.loads(b64url_decode(p)) for p in parts if p]

def extract_handshake_claims(jwt: str) -> dict:
    parts = jwt.split(".")
    if len(parts) < 2:
        raise ValueError("bad handshake jwt")
    return json.loads(b64url_decode(parts[1]))
