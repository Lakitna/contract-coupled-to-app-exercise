"""Local stub server for the Weather API.

Serves the provider interface fixtures in ``stub_server/stubs.json`` and appends one
line to ``stub_server/server.log`` for every request it handles, recording which stub (if
any) matched. Used by the test suite and as a standalone dev server.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, jsonify, request

STUBS_PATH = Path(__file__).resolve().parent / "stubs.json"
LOG_PATH = Path(__file__).resolve().parent / "server.log"


def load_stubs(path=STUBS_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _query_str(query_params):
    if not query_params:
        return ""
    joined = "&".join(f"{k}={v}" for k, v in sorted(query_params.items()))
    return f"?{joined}"


def _append_log(line):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _find_stub(stubs, method, path, query):
    q_norm = {str(k): str(v) for k, v in query.items()}
    for stub in stubs:
        if stub["method"].upper() != method.upper():
            continue
        if stub["path"] != path:
            continue
        sq = {str(k): str(v) for k, v in stub.get("query", {}).items()}
        if sq == q_norm:
            return stub
    return None


def create_app(stubs=None):
    app = Flask(__name__)
    app.json.compact = False  # type: ignore
    if stubs is None:
        stubs = load_stubs()

    @app.route("/", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    @app.route("/<path:sub>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
    def catch_all(sub=""):
        path = request.path
        method = request.method
        query = request.args.to_dict()
        stub = _find_stub(stubs, method, path, query)

        ts = _now_iso()
        target = f"{path}{_query_str(query)}"
        if stub is not None:
            desc = stub.get("description", "")
            _append_log(f"{ts} {method} {target} -> {stub['id']} {desc}".rstrip())
            resp = stub["response"]
            body = resp.get("json", resp.get("body", {}))
            return jsonify(body), resp.get("status", 200)

        _append_log(f"{ts} {method} {target} -> NO_MATCH")
        return jsonify({"error": "no matching stub", "path": path}), 404

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=8000, use_reloader=False)
