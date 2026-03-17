#!/usr/bin/env bash
set -o errexit

# Install Tailscale
curl -fsSL https://tailscale.com/install.sh | sh

# Connect to Tailscale network
if [ -n "$TAILSCALE_AUTH_KEY" ]; then
  sudo tailscale up --authkey=$TAILSCALE_AUTH_KEY --accept-routes
fi

# Regular build steps
pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
