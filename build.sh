#!/usr/bin/env bash
set -o errexit

# Install Tailscale
echo "📦 Installing Tailscale..."
curl -fsSL https://pkgs.tailscale.com/stable/tailscale_latest_amd64.tgz -o tailscale.tgz
tar xzf tailscale.tgz
mv tailscale_*_amd64/tailscale /tmp/tailscale
mv tailscale_*_amd64/tailscaled /tmp/tailscaled
chmod +x /tmp/tailscale /tmp/tailscaled
rm -rf tailscale.tgz tailscale_*_amd64

echo "✅ Tailscale binaries installed"

# Regular build (no Tailscale start during build)
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running migrations..."
python manage.py migrate

echo "✅ Build complete!"
