#!/usr/bin/env bash
set -o errexit

echo "==> Installing Tailscale..."
# (same tailscale setup as before)

# Connect to Tailscale
if [ -n "$TAILSCALE_AUTH_KEY" ]; then
    /tmp/tailscale-bin \
        --socket=/tmp/tailscale-socket/tailscaled.sock \
        up \
        --authkey="$TAILSCALE_AUTH_KEY" \
        --hostname=render-django \
        --accept-routes || echo "⚠️  Tailscale up failed"
else
    echo "❌ TAILSCALE_AUTH_KEY not set!"
fi

# Start Ollama
echo "🚀 Starting Ollama..."
curl -fsSL https://ollama.com/download/Ollama-linux-amd64.tgz -o /tmp/ollama.tgz
tar -xzf /tmp/ollama.tgz -C /tmp
chmod +x /tmp/ollama/ollama
/tmp/ollama/ollama serve &
sleep 5

# Preload Qwen model
echo "📦 Preloading Qwen model"
curl -X POST http://localhost:11434/api/pull -d '{"name":"qwen"}' || echo "⚠️ Model preload failed"

# Start Django (replace with your actual project name!)
echo "🌐 Starting Django application..."
exec gunicorn ai_learning_platform.wsgi:application
