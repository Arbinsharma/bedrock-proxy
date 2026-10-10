def apply_automine(packet_id, payload, cheat_state, ctx):
    if not cheat_state.get("automine"):
        return payload
    return payload
