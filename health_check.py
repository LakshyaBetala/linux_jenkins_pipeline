# health_check.py
import requests
import subprocess
import sys
import time

URL = "http://localhost:5001"
RETRIES = 3

def is_app_healthy():
    for i in range(RETRIES):
        try:
            r = requests.get(URL, timeout=3)
            if r.status_code == 200:
                print("✅ App is healthy!")
                return True
        except Exception as e:
            print(f"❌ Attempt {i+1}: {e}")
        time.sleep(2)
    return False

def redeploy():
    print("🚨 App unhealthy! Rebuilding container...")
    try:
        subprocess.run(
            ["sudo", "/usr/bin/podman", "rm", "-f", "myflask-staging"],
            check=False,
        )
        subprocess.run(
            ["sudo", "/usr/bin/podman", "run", "-d", "--name", "myflask-staging",
             "-p", "5001:5000", "localhost:5000/myflask:latest"],
            check=True,
        )
        print("✅ Redeployment completed.")
    except Exception as e:
        print(f"⚠️ Redeployment failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if not is_app_healthy():
        redeploy()
