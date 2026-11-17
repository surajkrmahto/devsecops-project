

from flask import Flask, jsonify, Response, request, g
import socket
import os
import time

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

app = Flask(__name__)

# Application state for self-healing demonstration
app_state = {
    "status": "healthy",
    "failure_mode": False,
    "started_at": time.strftime("%Y-%m-%d %H:%M:%S")
}

# Total HTTP requests by method, endpoint and status code
HTTP_REQUESTS = Counter(
    "flask_http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

# HTTP request duration in seconds
HTTP_REQUEST_DURATION = Histogram(
    "flask_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)


@app.before_request
def start_timer():
    g.start_time = time.time()


@app.after_request
def record_metrics(response):
    # Do not count the metrics endpoint itself
    if request.endpoint != "metrics":
        endpoint = request.endpoint or "unknown"
        method = request.method
        status = str(response.status_code)

        HTTP_REQUESTS.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()

        duration = time.time() - getattr(g, "start_time", time.time())

        HTTP_REQUEST_DURATION.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    return response


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


@app.route("/simulate-failure")
def simulate_failure():
    app_state["failure_mode"] = True
    app_state["status"] = "unhealthy"

    return jsonify({
        "message": "Failure simulation activated",
        "status": "unhealthy"
    }), 200


@app.route("/recover")
def recover():
    app_state["failure_mode"] = False
    app_state["status"] = "healthy"

    return jsonify({
        "message": "Application recovered successfully",
        "status": "healthy"
    }), 200


# Prometheus metrics endpoint
@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
