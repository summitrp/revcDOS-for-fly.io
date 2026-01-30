#@title ▶️ Start Server (Local) { display-mode: "form" }
import subprocess
import time
import sys
import os
from IPython.display import clear_output, display, HTML

PORT = 4000
LOCAL_URL = f"http://localhost:{PORT}"

# Clone repo
print("📥 Cloning repository...")
subprocess.run(
    ["git", "clone", "-q", "https://github.com/Lolendor/reVCDOS.git"],
    capture_output=True
)

os.chdir("reVCDOS")

# Install dependencies
print("📦 Installing dependencies...")
subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
    capture_output=True
)

# Start server
print("🚀 Starting server...")
server = subprocess.Popen(
    [sys.executable, "server.py", "--packed", "https://folder.morgen.qzz.io/revcdos.bin"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

time.sleep(3)

# Clear output and show UI
clear_output(wait=True)

html = f'''
<div style="font-family: Arial, sans-serif; padding: 24px; background:#202124; color:#e8eaed;
            border-radius: 12px; max-width: 600px; margin: auto;">
    <h2>Server is running locally</h2>
    <p style="color:#9aa0a6;">Open the game using your local server.</p>

    <div style="margin-bottom:16px;">
        <label>Language</label><br>
        <select id="lang">
            <option value="en">English</option>
            <option value="ru">Russian</option>
        </select>
    </div>

    <div style="margin-bottom:16px;">
        <label>Max FPS</label><br>
        <select id="max_fps">
            <option value="">Unlocked</option>
            <option value="30">30</option>
            <option value="60">60</option>
            <option value="120">120</option>
            <option value="240">240</option>
        </select>
    </div>

    <div style="margin-bottom:16px;">
        <label><input type="checkbox" id="cheats"> Enable Cheats</label><br>
        <label><input type="checkbox" id="req_orig"> Request Original Game Files</label><br>
        <label><input type="checkbox" id="fullscreen" checked> Auto Fullscreen</label>
    </div>

    <button onclick="launch()" style="
        background:#8ab4f8; color:#202124; border:none;
        padding:12px 24px; border-radius:24px; cursor:pointer;">
        Launch Game
    </button>

    <div style="margin-top:16px; font-size:13px;">
        URL: <code>{LOCAL_URL}</code>
    </div>
</div>

<script>
function launch() {{
    const lang = document.getElementById('lang').value;
    const cheats = document.getElementById('cheats').checked ? '&cheats=1' : '';
    const reqOrig = document.getElementById('req_orig').checked ? '&request_original_game=1' : '';
    const fullscreen = document.getElementById('fullscreen').checked ? '' : '&fullscreen=0';
    const maxFps = document.getElementById('max_fps').value
        ? '&max_fps=' + document.getElementById('max_fps').value
        : '';

    const url = `{LOCAL_URL}/?lang=${{lang}}${{cheats}}${{reqOrig}}${{fullscreen}}${{maxFps}}`;
    window.open(url, "_blank");
}}
</script>
'''

display(HTML(html))

# Keep server alive
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    server.terminate()
