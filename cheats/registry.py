CHEATS = {
    "fly":       {"default": False, "desc": "Allow airborne movement"},
    "speed":     {"default": False, "desc": "Scale movement deltas"},
    "automine":  {"default": False, "desc": "Auto break target block"},
    "noclip":    {"default": False, "desc": "Ignore collision"},
    "killaura":  {"default": False, "desc": "Auto-attack nearby entities"},
    "reach":     {"default": False, "desc": "Extended interact range"},
    "nofall":    {"default": False, "desc": "Cancel fall damage packets"},
    "scaffold":  {"default": False, "desc": "Auto-place under feet"},
    "antikick":  {"default": True,  "desc": "Suppress server kick"},
    "nolag":     {"default": True,  "desc": "Drop redundant packets"},
    "fastbreak": {"default": False, "desc": "Accelerate block break"},
    "secure":    {"default": True,  "desc": "Strip proxy artifacts"},
}

class CheatState:
    def __init__(self):
        self.state = {k: v["default"] for k, v in CHEATS.items()}

    def set(self, name, value):
        if name in self.state:
            self.state[name] = bool(value)
            return True
        return False

    def get(self, name):
        return self.state.get(name, False)

    def all(self):
        return dict(self.state)
