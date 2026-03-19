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

echo "🚀 Starting Tailscale daemon with SOCKS5 proxy on port 1055..."
/tmp/tailscaled-bin \
    --tun=userspace-networking \
    --socks5-server=localhost:1055 \
    --outbound-http-proxy-listen=localhost:1055 \
    --state=/tmp/tailscale-state/tailscaled.state \
    --socket=/tmp/tailscale-socket/tailscaled.sock \
    --statedir=/tmp/tailscale-state &

TAILSCALED_PID=$!
echo "✅ Tailscaled started with SOCKS5 on :1055 (PID: $TAILSCALED_PID)"
sleep 8

if [ -n "$TAILSCALE_AUTH_KEY" ]; then
    echo "🔗 Connecting to Tailscale network..."

    /tmp/tailscale-bin \
        --socket=/tmp/tailscale-socket/tailscaled.sock \
        up \
        --authkey="$TAILSCALE_AUTH_KEY" \
        --hostname=render-django \
        --accept-routes \
        --reset || echo "⚠️  Tailscale up failed"

    sleep 8

    echo "✅ Tailscale status:"
    /tmp/tailscale-bin --socket=/tmp/tailscale-socket/tailscaled.sock status

    echo "🧪 Testing Ollama via SOCKS5 proxy..."
    curl --socks5 localhost:1055 --max-time 20 http://100.111.210.32:11434 \
        && echo "✅ Ollama reachable via SOCKS5!" \
        || echo "❌ Ollama not reachable via SOCKS5"
else
    echo "❌ TAILSCALE_AUTH_KEY not set!"
fi

echo "🌐 Starting Django application..."
cd /opt/render/project/src

# ✅ FIX: timeout=300 gives LLM 5 minutes per request (was 30s default)
# ✅ graceful-timeout=300 allows slow LLM responses to finish
# ✅ keep-alive=5 handles connection reuse
exec gunicorn AIpoweredlearningplatform.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --timeout 300 \
    --graceful-timeout 300 \
    --keep-alive 5 \
    --workers 1 \
    --log-level info
