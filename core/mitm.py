import threading
import time
from util.net import make_udp_socket, addr_to_str
from core.raknet import RakNetSession
from chat.commands import handle_chat_command

class SessionCtx:
    def __init__(self, log, cheat_mgr):
        self.log = log
        self.cheat_mgr = cheat_mgr
        self.alive = True
        self.player_addr = None
        self.server_addr = None

class MITMSession(threading.Thread):
    def __init__(self, listen_sock, target_ip, target_port, log, cheat_mgr, idle_timeout, on_end):
        super().__init__(daemon=True)
        self.listen_sock = listen_sock
        self.target = (target_ip, target_port)
        self.log = log
        self.cheat_mgr = cheat_mgr
        self.idle_timeout = idle_timeout
        self.on_end = on_end
        self.ctx = SessionCtx(log, cheat_mgr)
        self.client_sock = None
        self.server_sock = None
        self.client_addr = None
        self.client_rak = RakNetSession(log)
        self.server_rak = RakNetSession(log)

    def run(self):
        try:
            self.log.info("Waiting for player to join proxy...")
            self.listen_sock.settimeout(None)
            data, addr = self.listen_sock.recvfrom(65535)
            self.client_addr = addr
            self.ctx.player_addr = addr
            self.log.info(f"Player joined: {addr_to_str(addr)}")

            self.client_sock = make_udp_socket(timeout=0.5)
            self.server_sock = make_udp_socket(timeout=0.5)
            self.ctx.server_addr = self.target
            self.server_sock.sendto(data, self.target)

            t1 = threading.Thread(target=self._client_to_server, daemon=True)
            t2 = threading.Thread(target=self._server_to_client, daemon=True)
            t1.start(); t2.start()

            while self.ctx.alive:
                if self.client_rak.is_dead(self.idle_timeout):
                    self.log.info("Client idle -> ending session")
                    break
                time.sleep(0.5)
        except Exception as e:
            self.log.error(f"session error: {e}")
        finally:
            self.ctx.alive = False
            for s in (self.client_sock, self.server_sock):
                try:
                    if s: s.close()
                except Exception: pass
            self.log.info("Session ended. Proxy stopped.")
            self.on_end()

    def _client_to_server(self):
        while self.ctx.alive:
            try:
                data, addr = self.client_sock.recvfrom(65535)
            except Exception:
                continue
            if not data:
                continue
            self.client_rak.touch()
            payload = self.client_rak.parse_datagram(data)
            if payload is None:
                self.server_sock.sendto(data, self.target)
                continue
            pkt_id = payload[0] if payload else -1
            payload = handle_chat_command(pkt_id, payload, self.cheat_mgr, self.ctx)
            if payload is None:
                continue
            payload = self.cheat_mgr.apply(pkt_id, payload, "c2s", self.ctx)
            if payload is None:
                continue
            out = self.client_rak.wrap_datagram(payload, reliable=True)
            self.server_sock.sendto(out, self.target)

    def _server_to_client(self):
        while self.ctx.alive:
            try:
                data, addr = self.server_sock.recvfrom(65535)
            except Exception:
                continue
            if not data:
                continue
            self.server_rak.touch()
            payload = self.server_rak.parse_datagram(data)
            if payload is None:
                self.client_sock.sendto(data, self.client_addr)
                continue
            pkt_id = payload[0] if payload else -1
            payload = self.cheat_mgr.apply(pkt_id, payload, "s2c", self.ctx)
            if payload is None:
                continue
            out = self.server_rak.wrap_datagram(payload, reliable=True)
            self.client_sock.sendto(out, self.client_addr)
