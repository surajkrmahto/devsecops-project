
import subprocess
import time
import urllib.request
from datetime import datetime

CONTAINER = "devsecops-container"
HEALTH_URL = "http://localhost:5000/health"
CHECK_INTERVAL = 10


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def container_status():
    result = subprocess.run(
        ["docker", "inspect", "-f",
         "{{.State.Status}}", CONTAINER],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        log("ERROR: Container not found")
        return "missing"

    return result.stdout.strip()


def application_healthy():
    try:
        with urllib.request.urlopen(
            HEALTH_URL, timeout=5
        ) as response:
            return response.status == 200
    except Exception:
        return False


def recover_container():
    log("Starting Docker container recovery")

    result = subprocess.run(
        ["docker", "start", CONTAINER],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        log("Container start command successful")
        return True

    log(f"Container recovery failed: {result.stderr}")
    return False


def main():
    log("Docker Self-Healing Controller Started")

    while True:
        status = container_status()
        log(f"Container status: {status}")

        if status in ["exited", "created"]:
            recover_container()

        elif status == "running":
            if application_healthy():
                log("Application HEALTHY")
            else:
                log("Application UNHEALTHY - restarting container")

                subprocess.run(
                    ["docker", "restart", CONTAINER],
                    check=False
                )

        elif status == "missing":
            log("Container does not exist. Manual investigation required.")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Controller stopped")
