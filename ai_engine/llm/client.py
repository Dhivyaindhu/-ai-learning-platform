# ai_engine/llm/client.py
# OLLAMA BACKEND: Uses local qwen-local model via Ollama server
# Routes through Tailscale SOCKS5 proxy on Render

import os
import requests


def _get_session():
    """
    Build a requests session.
    On Render (userspace Tailscale), traffic to 100.x.x.x must go
    through the SOCKS5 proxy that tailscaled exposes on localhost:1055.
    Locally, no proxy needed — direct localhost connection.
    """
    session = requests.Session()

    # Detect if we're running on Render (SOCKS5 proxy available)
    use_proxy = (
        os.environ.get("RENDER") or
        os.environ.get("TAILSCALE_AUTH_KEY") or
        os.environ.get("USE_SOCKS5_PROXY")
    )

    if use_proxy:
        proxy = os.environ.get("SOCKS5_PROXY", "socks5://localhost:1055")
        session.proxies = {
            "http":  proxy,
            "https": proxy,
        }
        print(f"🔌 Using SOCKS5 proxy: {proxy}")
    else:
        print(f"🔌 Direct connection (no proxy)")

    return session


class LocalLLM:

    DEFAULT_SYSTEM = (
        "You are a helpful assistant for an AI-powered learning platform. "
        "Follow instructions exactly and be concise."
    )

    def __init__(self, model_name="qwen-local"):
        self.model_name  = model_name
        self._connected  = False

        # Read Ollama URL from environment
        base = (
            os.environ.get("OLLAMA_URL") or
            os.environ.get("OLLAMA_BASE_URL") or
            "http://localhost:11434"
        )
        self.OLLAMA_BASE = base.rstrip("/")
        self.OLLAMA_URL  = f"{self.OLLAMA_BASE}/api/generate"
        self.session     = _get_session()

        print(f"🔄 Initializing Ollama client...")
        print(f"🔗 Ollama URL: {self.OLLAMA_BASE}")

        self._try_connect()

    def _try_connect(self):
        try:
            resp = self.session.get(self.OLLAMA_BASE, timeout=30)
            resp.raise_for_status()
            self._connected = True
            print(f"✅ Ollama server: running")
            print(f"✅ Model: {self.model_name}")
        except Exception as e:
            self._connected = False
            print(f"⚠️  Ollama not reachable at startup: {e}")
            print(f"   Will retry on first generate call.")

    def _ensure_connected(self):
        """Retry connection before each generate call."""
        if self._connected:
            return True
        try:
            resp = self.session.get(self.OLLAMA_BASE, timeout=20)
            resp.raise_for_status()
            self._connected = True
            print(f"✅ Ollama reconnected!")
            return True
        except Exception:
            return False

    def generate(
        self,
        prompt: str,
        max_tokens: int = 100,
        system_prompt: str = None,
    ) -> str:
        if not self._ensure_connected():
            print(f"❌ Ollama not reachable at {self.OLLAMA_BASE}")
            return ""

        try:
            sys_msg = system_prompt or self.DEFAULT_SYSTEM

            payload = {
                "model":  self.model_name,
                "prompt": prompt,
                "system": sys_msg,
                "stream": False,
                "options": {
                    "num_predict":    max_tokens,
                    "temperature":    0.7,
                    "top_k":          20,
                    "top_p":          0.9,
                    "repeat_penalty": 1.2,
                    "num_ctx":        1024,
                }
            }

            response = self.session.post(
                self.OLLAMA_URL,
                json=payload,
                timeout=180,
            )
            response.raise_for_status()
            result = response.json().get("response", "").strip()
            return result if result else ""

        except requests.exceptions.ConnectionError:
            self._connected = False
            print(f"❌ Ollama connection lost")
            return ""
        except requests.exceptions.Timeout:
            print(f"❌ Ollama request timed out")
            return ""
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return ""
