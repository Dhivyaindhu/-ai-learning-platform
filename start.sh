#!/usr/bin/env bash
set -o errexit

echo "🚀 Starting Tailscale..."

# Create directories we can write to
mkdir -p /tmp/tailscale
mkdir -p /tmp/tailscale-state

# Start tailscaled with CUSTOM SOCKET PATH
/tmp/tailscaled \
    --tun=userspace-networking \
    --state=/tmp/tailscale-state/tailscaled.state \
    --socket=/tmp/tailscale/tailscaled.sock \
    --statedir=/tmp/tailscale-state &

TAILSCALED_PID=$!
echo "✅ Tailscaled started (PID: $TAILSCALED_PID)"

# Wait for daemon to be ready
sleep 5

# Connect to Tailscale network
if [ -n "$TAILSCALE_AUTH_KEY" ]; then
    echo "🔗 Connecting to Tailscale network..."
    
    /tmp/tailscale \
        --socket=/tmp/tailscale/tailscaled.sock \
        up \
        --authkey="$TAILSCALE_AUTH_KEY" \
        --hostname=render-django \
        --accept-routes
    
    sleep 3
    
    echo "✅ Tailscale connected! Status:"
    /tmp/tailscale --socket=/tmp/tailscale/tailscaled.sock status
else
    echo "⚠️  TAILSCALE_AUTH_KEY not set - skipping Tailscale connection"
fi

# Start Django application
echo "🌐 Starting Django application..."
exec gunicorn AIpoweredlearningplatform.wsgi:application
