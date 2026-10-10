_seen = {}

def apply_nolag(packet_id, payload, cheat_state, ctx):
    if not cheat_state.get("nolag"):
        return payload
    key = (packet_id, hash(payload))
    if _seen.get(key):
        return None
    _seen[key] = True
    if len(_seen) > 4096:
        _seen.clear()
    return payload
