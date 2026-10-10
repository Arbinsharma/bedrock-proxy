from Crypto.Cipher import AES
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256

def derive_keys(shared_secret: bytes, salt: bytes):
    okm = HKDF(shared_secret, 32, salt, SHA256, 1)
    key = okm[:16]
    iv = okm[16:32]
    return key, iv

class GCMCodec:
    def __init__(self, key: bytes, iv: bytes):
        self.key = key
        self.iv = iv
        self.send_counter = 0
        self.recv_counter = 0

    def _nonce(self, counter: int) -> bytes:
        return self.iv + counter.to_bytes(8, "big")

    def encrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=self._nonce(self.send_counter))
        cipher.update(aad)
        ct, tag = cipher.encrypt_and_digest(data)
        self.send_counter += 1
        return ct + tag

    def decrypt(self, data: bytes, aad: bytes = b"") -> bytes:
        ct, tag = data[:-16], data[-16:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=self._nonce(self.recv_counter))
        cipher.update(aad)
        pt = cipher.decrypt_and_verify(ct, tag)
        self.recv_counter += 1
        return pt
