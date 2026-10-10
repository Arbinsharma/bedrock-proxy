def apply_nofall(packet_id, payload, cheat_state, ctx):
    if not cheat_state.get("nofall"):
        return payload
    return payload
