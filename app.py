
from flask import Flask, jsonify
import os
import socket
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of application requests"
)

@app.route("/")
def home():
    REQUEST_COUNT.inc()
    return """
    <html>
      <head><title>VLE7 DevOps Application</title></head>
      <body style="font-family:Arial;text-align:center;margin-top:100px">
        <h1>VLE7 DevOps Monitoring System</h1>
        <h2>Application is running!</h2>
        <p>Deployed using Jenkins, Docker and Kubernetes.</p>
        <p>Host: """ + socket.gethostname() + """</p>
      </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
