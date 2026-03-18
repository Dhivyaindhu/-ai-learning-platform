#!/usr/bin/env bash
set -o errexit

echo "==> Installing Tailscale..."

# Download and install Tailscale
curl -fsSL https://pkgs.tailscale.com/stable/tailscale_latest_amd64.tgz -o /tmp/tailscale.tgz
cd /tmp
tar xzf tailscale.tgz
chmod +x tailscale_*_amd64/tailscale tailscale_*_amd64/tailscaled
mv tailscale_*_amd64/tailscale /tmp/tailscale-bin
mv tailscale_*_amd64/tailscaled /tmp/tailscaled-bin
rm -rf tailscale.tgz tailscale_*_amd64

echo "✅ Tailscale binaries installed"

# Create directories
mkdir -p /tmp/tailscale-socket
mkdir -p /tmp/tailscale-state

# Start tailscaled
echo "🚀 Starting Tailscale daemon..."
/tmp/tailscaled-bin \
    --tun=userspace-networking \
    --state=/tmp/tailscale-state/tailscaled.state \
    --socket=/tmp/tailscale-socket/tailscaled.sock \
    --statedir=/tmp/tailscale-state &

TAILSCALED_PID=$!
echo "✅ Tailscaled started (PID: $TAILSCALED_PID)"

sleep 5

if ps -p $TAILSCALED_PID > /dev/null; then
   echo "✅ Tailscaled is running!"
else
   echo "❌ Tailscaled died!"
   exit 1
fi

# Connect to Tailscale
if [ -n "$TAILSCALE_AUTH_KEY" ]; then
    echo "🔗 Connecting to Tailscale network..."
    /tmp/tailscale-bin \
        --socket=/tmp/tailscale-socket/tailscaled.sock \
        up \
        --authkey="$TAILSCALE_AUTH_KEY" \
        --hostname=render-django \
        --accept-routes || echo "⚠️  Tailscale up failed (might already be connected)"
    sleep 3
    echo "✅ Tailscale status:"
    /tmp/tailscale-bin --socket=/tmp/tailscale-socket/tailscaled.sock status || echo "Status check failed"
else
    echo "❌ TAILSCALE_AUTH_KEY not set!"
fi

# Start Ollama
echo "🚀 Starting Ollama..."
curl -fsSL https://ollama.com/download/Ollama-linux-amd64.tgz -o /tmp/ollama.tgz
tar -xzf /tmp/ollama.tgz -C /tmp
chmod +x /tmp/ollama/ollama
/tmp/ollama/ollama serve &
OLLAMA_PID=$!
sleep 5

if ps -p $OLLAMA_PID > /dev/null; then
    echo "✅ Ollama started (PID: $OLLAMA_PID)"
else
    echo "❌ Ollama failed to start!"
    exit 1
fi

# Start Django
echo "🌐 Starting Django application..."
exec gunicorn AIpoweredlearningplatform.wsgi:application
