#!/usr/bin/env bash
set -o errexit

# Install Tailscale (static binary, no sudo needed!)
echo "📦 Installing Tailscale..."
curl -fsSL https://pkgs.tailscale.com/stable/tailscale_latest_amd64.tgz -o tailscale.tgz
tar xzf tailscale.tgz
mv tailscale_*_amd64/tailscale /tmp/tailscale
mv tailscale_*_amd64/tailscaled /tmp/tailscaled
chmod +x /tmp/tailscale /tmp/tailscaled

# Start tailscaled (doesn't need root)
echo "🚀 Starting Tailscale daemon..."
/tmp/tailscaled --tun=userspace-networking --state=/tmp/tailscaled.state &
sleep 3

# Connect to Tailscale network
if [ -n "$TAILSCALE_AUTH_KEY" ]; then
    echo "🔗 Connecting to Tailscale..."
    /tmp/tailscale up --authkey=$TAILSCALE_AUTH_KEY --hostname=render-django --accept-routes
    sleep 2
    echo "✅ Tailscale connected!"
    /tmp/tailscale status
else
    echo "⚠️  TAILSCALE_AUTH_KEY not set!"
fi

# Regular build
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running migrations..."
python manage.py migrate

echo "✅ Build complete!"
