from flask import Flask, render_template, jsonify, request

def create_app(manager, log):
    app = Flask(__name__, template_folder="templates", static_folder="static")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/status")
    def api_status():
        return jsonify({"status": manager.status(), "logs": log.tail(200)})

    @app.route("/api/config", methods=["POST"])
    def api_config():
        data = request.get_json(force=True)
        manager.update_config(
            target_ip=data.get("target_ip"),
            target_port=int(data["target_port"]) if data.get("target_port") else None,
            listen_host=data.get("listen_host"),
            listen_port=int(data["listen_port"]) if data.get("listen_port") else None,
        )
        return jsonify({"ok": True})

    @app.route("/api/cheat", methods=["POST"])
    def api_cheat():
        data = request.get_json(force=True)
        name = data.get("name")
        value = bool(data.get("value"))
        ok = manager.cheat_mgr.state.set(name, value)
        return jsonify({"ok": ok, "name": name, "value": value})

    @app.route("/api/start", methods=["POST"])
    def api_start():
        ok, msg = manager.start()
        return jsonify({"ok": ok, "msg": msg})

    @app.route("/api/stop", methods=["POST"])
    def api_stop():
        ok, msg = manager.stop()
        return jsonify({"ok": ok, "msg": msg})

    return app
