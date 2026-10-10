def apply_noclip(packet_id, payload, cheat_state, ctx):
    if not cheat_state.get("noclip"):
        return payload
    return payload
