#!/usr/bin/env python3
"""
reVCDOS Server - Render.com Deployment Version
Memory-safe packed file download
"""

import subprocess
import os
import sys
import requests

# Get PORT from environment variable
PORT = int(os.environ.get('PORT', 8000))

PACKED_URL = "https://folder.morgen.qzz.io/revcdos.bin"
PACKED_FILE = "revcdos.bin"

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

# Download packed file safely if it doesn't exist
if not os.path.exists(PACKED_FILE):
    print(f"📥 Downloading packed file from {PACKED_URL}...")
    with requests.get(PACKED_URL, stream=True) as r:
        r.raise_for_status()
        with open(PACKED_FILE, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    print(f"✅ Packed file downloaded: {PACKED_FILE}")
else:
    print(f"✅ Packed file already exists: {PACKED_FILE}")

# Set PORT environment variable for the server
os.environ['PORT'] = str(PORT)

# Start the server
print(f"🚀 Starting server on port {PORT}...")
print("=" * 60)

# Run server directly, using the already downloaded packed file
result = subprocess.run(
    [sys.executable, "server.py", "--packed", PACKED_FILE],
    env=os.environ
)

sys.exit(result.returncode)
