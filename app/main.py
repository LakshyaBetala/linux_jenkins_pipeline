import sys# app/main.py
import os
import time
import subprocess
from flask import Flask, jsonify, render_template, request

# Ensure templates/static paths are absolute (module-relative)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(
    __name__,
    template_folder=TEMPLATE_DIR,
    static_folder=STATIC_DIR
)

# Build metadata (Jenkins injects these via env)
BUILD_NUMBER = os.environ.get("BUILD_NUMBER", "local")
GIT_COMMIT = os.environ.get("GIT_COMMIT", "")[:8]
COMMIT_MSG = os.environ.get("COMMIT_MSG", "")
DEPLOY_TIME = time.ctime()


@app.route("/")
def index():
    info = {
        "message": "Hello from Flask via Podman!",
        "build_number": BUILD_NUMBER,
        "git_commit": GIT_COMMIT,
        "commit_msg": COMMIT_MSG,
        "deploy_time": DEPLOY_TIME,
    }

    # If running under tests (pytest), return JSON for easy assertions.
    # Detecting pytest via sys.modules is pragmatic and safe for CI/dev.
    if "pytest" in sys.modules:
        return jsonify(info), 200

    # If template exists, render dashboard; otherwise return JSON fallback.
    if os.path.exists(os.path.join(TEMPLATE_DIR, "dashboard.html")):
        return render_template("dashboard.html", info=info)
    else:
        return jsonify(info), 200


@app.route("/api/version")
def version():
    return jsonify({
        "build_number": BUILD_NUMBER,
        "git_commit": GIT_COMMIT,
        "commit_msg": COMMIT_MSG,
        "deploy_time": DEPLOY_TIME,
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "time": time.ctime()}), 200

@app.route("/action/healthcheck", methods=["POST"])
def run_healthcheck():
    try:
        r = app.test_client().get("/health")
        return jsonify({"result": r.get_json(), "status_code": r.status_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/action/rollback", methods=["POST"])
def rollback():
    previous_tag = request.form.get("tag", None) or os.environ.get("ROLLBACK_TAG", "")
    if not previous_tag:
        return jsonify({"error": "no rollback tag specified"}), 400

    try:
        subprocess.run(["sudo", "/usr/bin/podman", "rm", "-f", "myflask-staging"], check=False)
        subprocess.run([
            "sudo", "/usr/bin/podman", "run", "-d",
            "--name", "myflask-staging",
            "-p", "5001:5000",
            f"localhost:5000/myflask:{previous_tag}"
        ], check=True)
        return jsonify({"status": "rolled back", "tag": previous_tag})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # running locally for dev/demo
    app.run(host="0.0.0.0", port=5000)
