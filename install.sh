#!/bin/bash

# Fail on error
set -e

echo "Starting VocoBell installation..."

# Update and install system packages
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Deactivate virtualenv
deactivate

# Create systemd service
SERVICE_FILE="/etc/systemd/system/vocobell.service"

sudo bash -c "cat > $SERVICE_FILE" << EOF
[Unit]
Description=VocoBell Flask Server
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable vocobell.service
sudo systemctl start vocobell.service

echo "VocoBell installation complete. Server should now be running on port 5665."
