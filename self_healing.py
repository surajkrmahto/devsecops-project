
import time
import urllib.request
import urllib.error
from datetime import datetime

APP_URL = "http://localhost:5000"
CHECK_INTERVAL = 10


def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def check_application():
    try:
        with urllib.request.urlopen(
            f"{APP_URL}/health", timeout=5
        ) as response:
            if response.status == 200:
                log("Application is HEALTHY")
                return True

    except urllib.error.HTTPError as error:
        if error.code == 503:
            log("ALERT: Application is UNHEALTHY (503)")
        else:
            log(f"HTTP error detected: {error.code}")

    except Exception as error:
        log(f"Application connection failed: {error}")

    return False


def recover_application():
    try:
        log("Starting automatic recovery...")

        with urllib.request.urlopen(
            f"{APP_URL}/recover", timeout=5
        ) as response:
            if response.status == 200:
                log("RECOVERY SUCCESSFUL")
                return True

    except Exception as error:
        log(f"Recovery failed: {error}")

    return False


def main():
    log("Self-Healing Controller Started")

    while True:
        healthy = check_application()

        if not healthy:
            log("Initiating recovery action...")
            recover_application()

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("Self-Healing Controller Stopped")
