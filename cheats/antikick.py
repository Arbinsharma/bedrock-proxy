from core.protocol import PKT_DISCONNECT

def apply_antikick(packet_id, payload, cheat_state, ctx):
    if not cheat_state.get("antikick"):
        return payload
    if packet_id == PKT_DISCONNECT:
        ctx.log.warn("AntiKick: swallowed DisconnectPacket from server")
        return None
    return payload
