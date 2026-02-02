from flask import Flask, jsonify
import requests
import re

app = Flask(__name__)

@app.route("/api/start", methods=["GET"])
def start_server():
    # In Vercel, we can't run subprocesses persistently.
    # Instead, just return the remote server URL and password.
    
    # Tunnel URL (replace with a static service or your own deployment)
    tunnel_url = "https://your-tunnel-url.loca.lt"  # replace with real tunnel if you can
    # Tunnel password from remote endpoint
    try:
        password = requests.get("https://loca.lt/mytunnelpassword").text.strip()
    except Exception:
        password = "N/A"
    
    return jsonify({
        "tunnel_url": tunnel_url,
        "password": password
    })

# For Vercel, the entry point must be named `app`
app = app
