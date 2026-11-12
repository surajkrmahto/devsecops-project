from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "DevSecOps Self-Healing Application is Running!",
        "hostname": socket.gethostname(),
        "environment": os.getenv("ENVIRONMENT", "local")
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
