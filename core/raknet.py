import time

class RakNetSession:
    def __init__(self, log):
        self.log = log
        self.send_seq = 0
        self.recv_seq = 0
        self.last_seen = time.time()
        self.ack_queue = []

    def touch(self):
        self.last_seen = time.time()

    def is_dead(self, timeout=30):
        return (time.time() - self.last_seen) > timeout

    def wrap_datagram(self, payload: bytes, reliable=False) -> bytes:
        flags = 0x80
        if reliable:
            flags |= 0x40
        header = bytes([flags]) + self.send_seq.to_bytes(3, "little")
        self.send_seq = (self.send_seq + 1) & 0xFFFFFF
        return header + payload

    def parse_datagram(self, data: bytes):
        if len(data) < 4:
            return None
        seq = int.from_bytes(data[1:4], "little")
        self.recv_seq = max(self.recv_seq, seq)
        self.ack_queue.append(seq)
        return data[4:]

    def build_acks(self) -> bytes:
        if not self.ack_queue:
            return b""
        out = bytes([0xC0])
        out += len(self.ack_queue).to_bytes(2, "big")
        for s in self.ack_queue:
            out += s.to_bytes(3, "little") + b"\x01"
        self.ack_queue.clear()
        return out
