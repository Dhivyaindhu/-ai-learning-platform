#!/usr/bin/env bash
set -o errexit

echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running migrations..."
python manage.py migrate

echo "✅ Build complete!"
```

---

## 📤 **UPDATE ON GITHUB:**

1. Go to your GitHub repo
2. Edit `start.sh` - replace with the new code above
3. Edit `build.sh` - replace with the simplified version above
4. Commit changes

---

## 🔄 **MANUAL REDEPLOY:**

1. Render Dashboard → Your service
2. Click **"Manual Deploy"**
3. Select **"Clear build cache & deploy"**
4. Wait 3-5 minutes

---

## 📊 **NOW YOU SHOULD SEE:**
```
==> Running './start.sh'
==> Installing Tailscale...
✅ Tailscale binaries installed
🚀 Starting Tailscale daemon...
✅ Tailscaled started (PID: 123)
✅ Tailscaled is running!
🔗 Connecting to Tailscale network...
✅ Tailscale status:
100.64.12.34   render-django   connected
🌐 Starting Django application...
🚀 LLM Engine: INITIALIZING...
🔗 Ollama URL: http://100.111.210.32:11434
✅ Ollama server: running
✅ LLM ready: qwen-local via Ollama
==> Your service is live 🎉
