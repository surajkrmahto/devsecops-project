from flask import Flask, jsonify
import socket
import os
import time

app = Flask(__name__)

# Application state for self-healing demonstration
app_state = {
    "status": "healthy",
    "failure_mode": False,
    "started_at": time.strftime("%Y-%m-%d %H:%M:%S")
}


@app.route("/")
def home():
    return jsonify({
        "message": "DevSecOps Self-Healing Application is Running!",
        "hostname": socket.gethostname(),
        "environment": os.getenv("ENVIRONMENT", "local"),
        "status": app_state["status"]
    })


@app.route("/health")
def health():
    if app_state["failure_mode"]:
        return jsonify({
            "status": "unhealthy",
            "message": "Application failure detected"
        }), 503

    return jsonify({
        "status": "healthy",
        "message": "Application is running normally"
    }), 200


@app.route("/status")
def status():
    return jsonify({
        "application": "DevSecOps Self-Healing Application",
        "status": app_state["status"],
        "failure_mode": app_state["failure_mode"],
        "hostname": socket.gethostname(),
        "started_at": app_state["started_at"]
    }), 200


# Controlled failure simulation for project demonstration
@app.route("/simulate-failure")
def simulate_failure():
    app_state["failure_mode"] = True
    app_state["status"] = "unhealthy"

    return jsonify({
        "message": "Failure simulation activated",
        "status": "unhealthy"
    }), 200


# Recover application manually (useful for testing)
@app.route("/recover")
def recover():
    app_state["failure_mode"] = False
    app_state["status"] = "healthy"

    return jsonify({
        "message": "Application recovered successfully",
        "status": "healthy"
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
