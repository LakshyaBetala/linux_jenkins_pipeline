from flask import Flask, jsonify, render_template, request, redirect, url_for
import os
import subprocess
import time

app = Flask(__name__, template_folder='templates', static_folder='static')

# Read build metadata from environment (set by Jenkins)
BUILD_NUMBER = os.environ.get('BUILD_NUMBER', 'local')
GIT_COMMIT = os.environ.get('GIT_COMMIT', '')[:8]
COMMIT_MSG = os.environ.get('COMMIT_MSG', '')
DEPLOY_TIME = time.ctime()

@app.route('/')
def index():
    info = {
        "message": "Hello from Flask via Podman!",
        "build_number": BUILD_NUMBER,
        "git_commit": GIT_COMMIT,
        "commit_msg": COMMIT_MSG,
        "deploy_time": DEPLOY_TIME,
    }
    return render_template('dashboard.html', info=info)

@app.route('/api/version')
def version():
    return jsonify({
        "build_number": BUILD_NUMBER,
        "git_commit": GIT_COMMIT,
        "commit_msg": COMMIT_MSG,
        "deploy_time": DEPLOY_TIME,
    })

@app.route('/health')
def health():
    # simple health check for demo — extend as needed
    return jsonify({"status": "ok", "time": time.ctime()}), 200

@app.route('/action/healthcheck', methods=['POST'])
def run_healthcheck():
    """Optionally call the Jenkins health-monitor job or run an inline check.
       For demo, we'll simply call /health endpoint and return result."""
    try:
        r = app.test_client().get('/health')
        return jsonify({"result": r.get_json(), "status_code": r.status_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/action/rollback', methods=['POST'])
def rollback():
    """Manual rollback endpoint for demo — returns status only.
       NOTE: This runs podman commands and requires Jenkins sudoers or similar.
       Use with caution; consider restricting in production."""
    previous_tag = request.form.get('tag', None) or os.environ.get('ROLLBACK_TAG', '')
    if not previous_tag:
        return jsonify({"error": "no rollback tag specified"}), 400

    try:
        # stop current
        subprocess.run(["sudo", "/usr/bin/podman", "rm", "-f", "myflask-staging"], check=False)
        # run previous
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
    app.run(host='0.0.0.0', port=5000)
