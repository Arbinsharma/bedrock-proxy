def apply_fastbreak(packet_id, payload, cheat_state, ctx):
    if not cheat_state.get("fastbreak"):
        return payload
    return payload
