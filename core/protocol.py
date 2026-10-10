from io import BytesIO

PKT_LOGIN = 0x01
PKT_PLAY_STATUS = 0x02
PKT_DISCONNECT = 0x05
PKT_START_GAME = 0x0B
PKT_MOVE_PLAYER = 0x13
PKT_PLAYER_AUTH_INPUT = 0x90
PKT_TEXT = 0x09
PKT_COMMAND_REQUEST = 0x4D
PKT_INTERACT = 0x21
PKT_PLAYER_ACTION = 0x24
PKT_ANIMATE = 0x2C
PKT_RESPAWN = 0x2D
PKT_SET_ENTITY_DATA = 0x27
PKT_ADD_PLAYER = 0x0C
PKT_REMOVE_ENTITY = 0x0E

def read_varint(buf: BytesIO) -> int:
    val = 0
    for i in range(5):
        b = buf.read(1)
        if not b: raise EOFError
        b = b[0]
        val |= (b & 0x7F) << (7 * i)
        if not (b & 0x80):
            return val
    raise ValueError("varint too big")

def write_varint(value: int) -> bytes:
    out = b""
    while True:
        b = value & 0x7F
        value >>= 7
        if value:
            out += bytes([b | 0x80])
        else:
            out += bytes([b])
            return out
