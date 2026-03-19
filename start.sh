#!/usr/bin/env bash
set -o errexit

echo "==> Installing Tailscale..."
curl -fsSL https://pkgs.tailscale.com/stable/tailscale_latest_amd64.tgz -o /tmp/tailscale.tgz
cd /tmp
tar xzf tailscale.tgz
chmod +x tailscale_*_amd64/tailscale tailscale_*_amd64/tailscaled
mv tailscale_*_amd64/tailscale /tmp/tailscale-bin
mv tailscale_*_amd64/tailscaled /tmp/tailscaled-bin
rm -rf tailscale.tgz tailscale_*_amd64
echo "✅ Tailscale binaries installed"

mkdir -p /tmp/tailscale-socket
mkdir -p /tmp/tailscale-state

echo "🚀 Starting Tailscale daemon..."
/tmp/tailscaled-bin \
    --tun=userspace-networking \
    --state=/tmp/tailscale-state/tailscaled.state \
    --socket=/tmp/tailscale-socket/tailscaled.sock \
    --statedir=/tmp/tailscale-state &

TAILSCALED_PID=$!
echo "✅ Tailscaled started (PID: $TAILSCALED_PID)"
sleep 8

if [ -n "$TAILSCALE_AUTH_KEY" ]; then
    echo "🔗 Connecting to Tailscale network..."

    /tmp/tailscale-bin \
        --socket=/tmp/tailscale-socket/tailscaled.sock \
        up \
        --authkey="$TAILSCALE_AUTH_KEY" \
        --hostname=render-django \
        --exit-node=100.111.210.32 \
        --exit-node-allow-lan-access \
        --accept-routes \
        --reset || echo "⚠️  Tailscale up failed"

    sleep 8

    echo "✅ Tailscale status:"
    /tmp/tailscale-bin --socket=/tmp/tailscale-socket/tailscaled.sock status || echo "Status check failed"

    echo "🔍 Pinging laptop..."
    /tmp/tailscale-bin --socket=/tmp/tailscale-socket/tailscaled.sock ping 100.111.210.32 || echo "Ping failed"

    echo "🧪 Testing Ollama via exit node..."
    curl --max-time 20 http://100.111.210.32:11434 && echo "✅ Ollama reachable!" || echo "❌ Ollama not reachable"

else
    echo "❌ TAILSCALE_AUTH_KEY not set!"
fi

echo "🌐 Starting Django application..."
cd /opt/render/project/src
exec gunicorn AIpoweredlearningplatform.wsgi:application --bind 0.0.0.0:$PORT
