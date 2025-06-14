#!/bin/bash

# Fail on error
set -e

echo "Starting VocoBell installation..."

# Update and install system packages
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git nginx openssl alsa-utils

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn

# Deactivate virtualenv
deactivate

# Create systemd service for Gunicorn
SERVICE_FILE="/etc/systemd/system/vocobell.service"

sudo bash -c "cat > $SERVICE_FILE" << EOF
[Unit]
Description=VocoBell Flask Server via Gunicorn
After=network.target

[Service]
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 main:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable vocobell.service
sudo systemctl start vocobell.service

echo "Gunicorn Flask server running..."

# Generate self-signed certificate if not exists
SSL_CERT="/etc/ssl/certs/vocobell.crt"
SSL_KEY="/etc/ssl/private/vocobell.key"

if [ ! -f "$SSL_CERT" ] || [ ! -f "$SSL_KEY" ]; then
  echo "Generating self-signed SSL certificate..."
  sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$SSL_KEY" \
    -out "$SSL_CERT" \
    -subj "/CN=localhost"
fi

# Create NGINX config
NGINX_CONF="/etc/nginx/sites-available/vocobell"

sudo bash -c "cat > $NGINX_CONF" << EOF
server {
    listen 80;
    server_name _;

    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name _;

    ssl_certificate $SSL_CERT;
    ssl_certificate_key $SSL_KEY;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable NGINX site
if [ ! -L /etc/nginx/sites-enabled/vocobell ]; then
  sudo ln -s $NGINX_CONF /etc/nginx/sites-enabled/vocobell
fi

# Disable default nginx config if still enabled
if [ -f /etc/nginx/sites-enabled/default ]; then
  sudo rm /etc/nginx/sites-enabled/default
fi

# Test nginx and reload
sudo nginx -t
sudo systemctl reload nginx

echo "VocoBell installation complete."
echo "Your server should now be running at: https://<your-local-ip>/"
