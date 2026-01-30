#!/usr/bin/env python3
"""
reVCDOS Server - Render.com Deployment Version
This version is for deployment platforms, NOT for Colab
"""

import subprocess
import os
import sys

# Get PORT from environment variable
PORT = int(os.environ.get('PORT', 8000))

print("=" * 60)
print("🎮 reVCDOS Server - Deployment Mode")
print(f"📍 Port: {PORT}")
print("=" * 60)

# Clone repo if not already there
if not os.path.exists('reVCDOS'):
    print("📥 Cloning repository...")
    result = subprocess.run(
        ["git", "clone", "-q", "https://github.com/Lolendor/reVCDOS.git"],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"❌ Clone failed: {result.stderr}")
        sys.exit(1)
    print("✅ Repository cloned")

# Change to repo directory
os.chdir("reVCDOS")

# Install dependencies
print("📦 Installing dependencies...")
result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
    capture_output=True,
    text=True
)
if result.returncode != 0:
    print(f"⚠️  Installation warnings: {result.stderr}")
else:
    print("✅ Dependencies installed")

# Set PORT environment variable for the actual server
os.environ['PORT'] = str(PORT)

# Start the server (without localtunnel, without IPython stuff)
print(f"🚀 Starting server on port {PORT}...")
print("=" * 60)

# Run server directly with output visible
result = subprocess.run(
    [sys.executable, "server.py", "--packed", "https://folder.morgen.qzz.io/revcdos.bin"],
    env=os.environ
)

sys.exit(result.returncode)
