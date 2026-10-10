import time
import threading

class Logger:
    def __init__(self, max_lines=500):
        self.lines = []
        self.max = max_lines
        self.lock = threading.Lock()

    def _push(self, level, msg):
        stamp = time.strftime("%H:%M:%S")
        line = f"[{stamp}] [{level}] {msg}"
        with self.lock:
            self.lines.append(line)
            if len(self.lines) > self.max:
                self.lines = self.lines[-self.max:]
        print(line)

    def info(self, msg): self._push("INFO", msg)
    def warn(self, msg): self._push("WARN", msg)
    def error(self, msg): self._push("ERR ", msg)

    def tail(self, n=200):
        with self.lock:
            return self.lines[-n:]

