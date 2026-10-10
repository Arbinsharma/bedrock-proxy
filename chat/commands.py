from core.protocol import PKT_TEXT

PREFIX = "."

def handle_chat_command(packet_id, payload, cheat_mgr, ctx):
    if packet_id != PKT_TEXT:
        return payload
    try:
        raw = payload.decode("utf-8", errors="ignore")
        if PREFIX not in raw:
            return payload
        idx = raw.find(PREFIX)
        msg = raw[idx:].strip().split("\x00")[0]
        parts = msg.split()
        if not parts:
            return payload
        cmd = parts[0][len(PREFIX):].lower()
        if cmd in cheat_mgr.state.state:
            if len(parts) > 1:
                val = parts[1].lower() in ("on", "1", "true", "yes")
            else:
                val = not cheat_mgr.state.get(cmd)
            cheat_mgr.state.set(cmd, val)
            ctx.log.info(f"Chat command: {cmd} -> {'ON' if val else 'OFF'}")
            return None
    except Exception as e:
        ctx.log.error(f"chat parse error: {e}")
    return payload
