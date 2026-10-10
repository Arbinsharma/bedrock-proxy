from web.app import create_app
from core.manager import ProxyManager
from util.logger import Logger

log = Logger()

def main():
    log.info("AlphA Bedrock Proxy starting...")
    manager = ProxyManager(log)
    app = create_app(manager, log)
    log.info("Panel on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, threaded=True, use_reloader=False)

if __name__ == "__main__":
    main()
