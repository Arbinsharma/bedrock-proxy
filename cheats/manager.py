from cheats.registry import CheatState
from cheats import (
    fly, speed, automine, noclip, killaura, reach,
    nofall, scaffold, antikick, nolag, fastbreak, secure
)

PIPELINE = [
    secure, nolag, antikick,
    fly, speed, automine, noclip, killaura, reach,
    nofall, scaffold, fastbreak,
]

class CheatManager:
    def __init__(self):
        self.state = CheatState()

    def apply(self, packet_id, payload, direction, ctx):
        if payload is None:
            return None
        for mod in PIPELINE:
            name = mod.__name__.split(".")[-1]
            fn = getattr(mod, f"apply_{name}", None)
            if fn is None:
                continue
            try:
                payload = fn(packet_id, payload, self.state, ctx)
            except Exception as e:
                ctx.log.error(f"cheat {name} error: {e}")
            if payload is None:
                return None
        return payload
