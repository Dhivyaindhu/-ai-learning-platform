#!/usr/bin/env bash
set -o errexit

# Install Tailscale (without sudo)
curl -fsSL https://tailscale.com/install.sh | sh

# Start Tailscale (Render runs as root, so no sudo needed)
if [ -n "$TAILSCALE_AUTH_KEY" ]; then
  tailscale up --authkey=$TAILSCALE_AUTH_KEY --accept-routes --hostname=render-ai-platform
fi

# Regular build steps
pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
