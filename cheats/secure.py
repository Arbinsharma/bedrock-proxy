def apply_secure(packet_id, payload, cheat_state, ctx):
    if not cheat_state.get("secure"):
        return payload
    return payload
