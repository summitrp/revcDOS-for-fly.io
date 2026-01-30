#@title ▶️ Start Server { display-mode: "form" }
import subprocess
import time
import urllib.request
import re
import sys
from IPython.display import clear_output, display, HTML

import os

# USE ENVIRONMENT VARIABLE FOR PORT (instead of hardcoded 8000)
PORT = int(os.environ.get('PORT', 8000))

# Clone repo
print("📥 Cloning repository...")
subprocess.run(["git", "clone", "-q", "https://github.com/Lolendor/reVCDOS.git"],
               capture_output=True)

os.chdir("reVCDOS")

# Install dependencies
print("📦 Installing dependencies...")
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
               capture_output=True)

# Install localtunnel
print("🌐 Installing localtunnel...")
subprocess.run(["npm", "install", "-g", "localtunnel"], capture_output=True)

# Get tunnel password from localtunnel's own endpoint
password = urllib.request.urlopen('https://loca.lt/mytunnelpassword').read().decode('utf8').strip()

# Start server
print("🚀 Starting server...")
server = subprocess.Popen(
    [sys.executable, "server.py", "--packed", "https://folder.morgen.qzz.io/revcdos.bin"],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
time.sleep(3)

# Start localtunnel and capture URL
print("🔗 Creating tunnel...")
tunnel = subprocess.Popen(
    ["lt", "--port", str(PORT)],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True
)

# Wait for URL
tunnel_url = None
for _ in range(30):
    line = tunnel.stdout.readline()
    if line:
        match = re.search(r'https://[a-zA-Z0-9-]+\.loca\.lt', line)
        if match:
            tunnel_url = match.group(0)
            break
    time.sleep(0.5)

# Clear all output and show only what matters
clear_output(wait=True)

if tunnel_url:
    # Display interactive button that copies password and opens URL
    html = f'''
    <div style="font-family: 'Google Sans', Roboto, Arial, sans-serif; padding: 24px; background-color: #202124; border: 1px solid #3c4043; border-radius: 12px; text-align: center; max-width: 600px; margin: 10px auto; box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);">
        <div style="color: #e8eaed; font-size: 22px; font-weight: 500; margin-bottom: 8px;">Server is ready</div>
        <div style="color: #9aa0a6; font-size: 14px; margin-bottom: 24px;">The tunnel is active. Configure options and launch the game.</div>

        <div style="margin-bottom: 24px; display: flex; justify-content: center; gap: 24px; align-items: flex-start; flex-wrap: wrap;">
            <div style="text-align: left;">
                <label style="color: #9aa0a6; font-size: 12px; display: block; margin-bottom: 6px; font-weight: 500;">Language</label>
                <div style="position: relative;">
                    <select id="lang" style="
                        appearance: none;
                        background: #202124;
                        color: #e8eaed;
                        border: 1px solid #5f6368;
                        border-radius: 4px;
                        padding: 8px 32px 8px 12px;
                        font-size: 14px;
                        outline: none;
                        cursor: pointer;
                        font-family: inherit;
                    " onmouseover="this.style.borderColor='#dadce0'" onmouseout="this.style.borderColor='#5f6368'">
                        <option value="en">English</option>
                        <option value="ru">Russian</option>
                    </select>
                    <div style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); pointer-events: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #9aa0a6;"></div>
                </div>
            </div>
            <div style="text-align: left;">
                <label style="color: #9aa0a6; font-size: 12px; display: block; margin-bottom: 6px; font-weight: 500;">Max FPS</label>
                <div style="position: relative;">
                    <select id="max_fps" style="
                        appearance: none;
                        background: #202124;
                        color: #e8eaed;
                        border: 1px solid #5f6368;
                        border-radius: 4px;
                        padding: 8px 32px 8px 12px;
                        font-size: 14px;
                        outline: none;
                        cursor: pointer;
                        font-family: inherit;
                    " onmouseover="this.style.borderColor='#dadce0'" onmouseout="this.style.borderColor='#5f6368'" onchange="document.getElementById('custom_fps_container').style.display = this.value === 'custom' ? 'block' : 'none'">
                        <option value="">Unlocked</option>
                        <option value="30">30 FPS</option>
                        <option value="60">60 FPS</option>
                        <option value="120">120 FPS</option>
                        <option value="240">240 FPS</option>
                        <option value="custom">Custom</option>
                    </select>
                    <div style="position: absolute; right: 10px; top: 50%; transform: translateY(-50%); pointer-events: none; border-left: 4px solid transparent; border-right: 4px solid transparent; border-top: 5px solid #9aa0a6;"></div>
                </div>
                <div id="custom_fps_container" style="display: none; margin-top: 8px;">
                    <input type="number" id="custom_fps" min="1" max="240" placeholder="1-240" style="
                        background: #202124;
                        color: #e8eaed;
                        border: 1px solid #5f6368;
                        border-radius: 4px;
                        padding: 8px 12px;
                        font-size: 14px;
                        outline: none;
                        width: 80px;
                        font-family: inherit;
                    " onmouseover="this.style.borderColor='#dadce0'" onmouseout="this.style.borderColor='#5f6368'">
                </div>
            </div>
            <div style="text-align: left;">
                <label style="color: #9aa0a6; font-size: 12px; display: block; margin-bottom: 6px; font-weight: 500;">Options</label>
                <label style="display: flex; align-items: center; cursor: pointer; color: #e8eaed; font-size: 14px;">
                    <input type="checkbox" id="cheats" style="
                        appearance: none;
                        width: 18px;
                        height: 18px;
                        border: 2px solid #9aa0a6;
                        border-radius: 2px;
                        margin-right: 8px;
                        position: relative;
                        cursor: pointer;
                        outline: none;
                    " onchange="this.style.backgroundColor = this.checked ? '#8ab4f8' : 'transparent'; this.style.borderColor = this.checked ? '#8ab4f8' : '#9aa0a6';">
                    Enable Cheats Menu (F3)
                </label>
                <label style="display: flex; align-items: center; cursor: pointer; color: #e8eaed; font-size: 14px; margin-top: 8px;">
                    <input type="checkbox" id="req_orig" style="
                        appearance: none;
                        width: 18px;
                        height: 18px;
                        border: 2px solid #9aa0a6;
                        border-radius: 2px;
                        margin-right: 8px;
                        position: relative;
                        cursor: pointer;
                        outline: none;
                    " onchange="this.style.backgroundColor = this.checked ? '#8ab4f8' : 'transparent'; this.style.borderColor = this.checked ? '#8ab4f8' : '#9aa0a6';">
                    Request Original Game Files
                </label>
                <label style="display: flex; align-items: center; cursor: pointer; color: #e8eaed; font-size: 14px; margin-top: 8px;">
                    <input type="checkbox" id="fullscreen" checked style="
                        appearance: none;
                        width: 18px;
                        height: 18px;
                        border: 2px solid #9aa0a6;
                        border-radius: 2px;
                        margin-right: 8px;
                        position: relative;
                        cursor: pointer;
                        outline: none;
                        background-color: #8ab4f8;
                        border-color: #8ab4f8;
                    " onchange="this.style.backgroundColor = this.checked ? '#8ab4f8' : 'transparent'; this.style.borderColor = this.checked ? '#8ab4f8' : '#9aa0a6';">
                    Auto Fullscreen
                </label>
            </div>
        </div>

        <button onclick="copyAndOpen()" style="
            background-color: #8ab4f8;
            color: #202124;
            border: none;
            padding: 12px 32px;
            font-size: 14px;
            font-weight: 500;
            border-radius: 24px;
            cursor: pointer;
            transition: background-color 0.2s, box-shadow 0.2s;
            outline: none;
        " onmouseover="this.style.backgroundColor='#aecbfa';this.style.boxShadow='0 1px 3px 0 rgba(60,64,67,0.3), 0 4px 8px 3px rgba(60,64,67,0.15)'"
           onmouseout="this.style.backgroundColor='#8ab4f8';this.style.boxShadow='none'">
            Launch Game
        </button>

        <div id="status" style="color: #8ab4f8; margin-top: 16px; font-size: 13px; height: 20px;"></div>

        <div style="margin-top: 24px; padding: 16px; background-color: #292a2d; border-radius: 8px; text-align: left; border: 1px solid #3c4043;">
            <div style="margin-bottom: 8px;">
                <span style="color: #9aa0a6; font-size: 12px; display: block; margin-bottom: 2px;">Tunnel URL</span>
                <span style="color: #8ab4f8; font-size: 14px; word-break: break-all;">{tunnel_url}</span>
            </div>
            <div>
                <span style="color: #9aa0a6; font-size: 12px; display: block; margin-bottom: 2px;">Tunnel Password</span>
                <span style="color: #e8eaed; font-size: 14px; font-family: monospace;">{password}</span>
            </div>
        </div>
    </div>
    <script>
        function copyAndOpen() {{
            const lang = document.getElementById('lang').value;
            const cheats = document.getElementById('cheats').checked ? '&cheats=1' : '';
            const reqOrig = document.getElementById('req_orig').checked ? '&request_original_game=1' : '';
            const fullscreen = document.getElementById('fullscreen').checked ? '' : '&fullscreen=0';
            const maxFpsSelect = document.getElementById('max_fps').value;
            let maxFps = '';
            if (maxFpsSelect === 'custom') {{
                const customVal = document.getElementById('custom_fps').value;
                if (customVal && parseInt(customVal) >= 1 && parseInt(customVal) <= 240) {{
                    maxFps = '&max_fps=' + customVal;
                }}
            }} else if (maxFpsSelect) {{
                maxFps = '&max_fps=' + maxFpsSelect;
            }}
            const finalUrl = `{tunnel_url}/?lang=${{lang}}${{cheats}}${{reqOrig}}${{fullscreen}}${{maxFps}}`;

            navigator.clipboard.writeText("{password}").then(function() {{
                document.getElementById("status").innerHTML = "✓ Password copied! Opening game...";
                setTimeout(function() {{
                    window.open(finalUrl, "_blank");
                }}, 500);
            }}).catch(function() {{
                document.getElementById("status").innerHTML = "Password: {password} (copy manually)";
                window.open(finalUrl, "_blank");
            }});
        }}
    </script>
    '''
    display(HTML(html))
else:
    print("❌ Failed to get tunnel URL")

# Keep running
try:
    while tunnel.poll() is None:
        time.sleep(10)
except KeyboardInterrupt:
    tunnel.terminate()
    server.terminate()
