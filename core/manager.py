import threading
import time
from util.net import make_udp_socket
from cheats.manager import CheatManager
from core.mitm import MITMSession

class ProxyManager:
    def __init__(self, log):
        self.log = log
        self.cheat_mgr = CheatManager()
        self.state = "IDLE"
        self.session = None
        self.listen_sock = None
        self.lock = threading.Lock()
        self.config = {
            "target_ip": "127.0.0.1",
            "target_port": 19132,
            "listen_host": "127.0.0.1",
            "listen_port": 19132,
            "session_idle_timeout_sec": 30,
        }

    def update_config(self, **kwargs):
        with self.lock:
            for k, v in kwargs.items():
                if v is not None:
                    self.config[k] = v
        self.log.info(f"Config updated: {kwargs}")

    def start(self):
        with self.lock:
            if self.state in ("LISTENING", "ACTIVE"):
                return False, "already running"
            self.listen_sock = make_udp_socket(
                bind_host=self.config["listen_host"],
                bind_port=self.config["listen_port"],
                timeout=None,
            )
            self.state = "LISTENING"
        self.log.info(f"Listening on {self.config['listen_host']}:{self.config['listen_port']} -> "
                      f"{self.config['target_ip']}:{self.config['target_port']}")
        self.session = MITMSession(
            listen_sock=self.listen_sock,
            target_ip=self.config["target_ip"],
            target_port=self.config["target_port"],
            log=self.log,
            cheat_mgr=self.cheat_mgr,
            idle_timeout=self.config["session_idle_timeout_sec"],
            on_end=self._on_session_end,
        )
        self.session.start()
        return True, "started"

    def _on_session_end(self):
        with self.lock:
            self.state = "ENDED"
        def _reset():
            time.sleep(1)
            with self.lock:
                if self.state == "ENDED":
                    self.state = "IDLE"
            self.log.info("Proxy reset -> IDLE")
        threading.Thread(target=_reset, daemon=True).start()

    def stop(self):
        with self.lock:
            if self.session:
                self.session.ctx.alive = False
            if self.listen_sock:
                try: self.listen_sock.close()
                except Exception: pass
                self.listen_sock = None
            self.state = "IDLE"
        self.log.info("Proxy manually stopped")
        return True, "stopped"

    def status(self):
        return {
            "state": self.state,
            "target": f"{self.config['target_ip']}:{self.config['target_port']}",
            "listen": f"{self.config['listen_host']}:{self.config['listen_port']}",
            "cheats": self.cheat_mgr.state.all(),
            "player": (str(self.session.client_addr) if self.session and self.session.client_addr else None),
        }
