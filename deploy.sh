#!/bin/bash

set -e

echo "Pulling latest code..."
git pull origin main

echo "Activating virtualenv..."
source venv/bin/activate

echo "Installing any updated requirements..."
pip install -r requirements.txt

echo "Restarting vocobell service..."
sudo systemctl restart vocobell.service

echo "Deployment complete."
