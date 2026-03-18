# ai_engine/llm/client.py
# OLLAMA BACKEND: Uses local qwen-local model via Ollama server

import os
import requests


class LocalLLM:

    DEFAULT_SYSTEM = (
        "You are a helpful assistant for an AI-powered learning platform. "
        "Follow instructions exactly and be concise."
    )

    def __init__(self, model_name="qwen-local"):
        self.model_name = model_name

        # ✅ FIX 1: Read Ollama URL from environment variable
        # - Locally:  http://localhost:11434  (default)
        # - On Render: http://100.111.210.32:11434 (set via OLLAMA_URL env var)
        base = os.environ.get("OLLAMA_URL", "http://localhost:11434").rstrip("/")
        self.OLLAMA_BASE = base
        self.OLLAMA_URL  = f"{base}/api/generate"

        print(f"🔄 Initializing Ollama client...")
        print(f"🔗 Ollama URL: {self.OLLAMA_BASE}")

        # ✅ FIX 2: Increase connect timeout from 5s to 30s
        # Tailscale tunnel needs more time to route the first request
        try:
            resp = requests.get(self.OLLAMA_BASE, timeout=30)
            resp.raise_for_status()
            print(f"✅ Ollama server: running")
            print(f"✅ Model: {model_name}")
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Ollama server not running!")
            print(f"   URL: {self.OLLAMA_BASE}")
            print(f"   Error: {e}")
            raise
        except requests.exceptions.Timeout:
            print(f"❌ Ollama server timed out after 30s!")
            print(f"   URL: {self.OLLAMA_BASE}")
            print(f"   Check: Is Ollama running? Is Tailscale connected?")
            raise
        except Exception as e:
            print(f"❌ Ollama connection error: {e}")
            raise

    def generate(
        self,
        prompt: str,
        max_tokens: int = 100,
        system_prompt: str = None,
    ) -> str:
        try:
            sys_msg = system_prompt if system_prompt is not None else self.DEFAULT_SYSTEM

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

            # ✅ FIX 3: Use self.OLLAMA_URL (env-aware) instead of hardcoded localhost
            response = requests.post(
                self.OLLAMA_URL,
                json=payload,
                timeout=180,  # increased from 120 — model inference can be slow on CPU
            )
            response.raise_for_status()
            result = response.json().get("response", "").strip()
            return result if result else ""

        except requests.exceptions.ConnectionError:
            print(f"❌ Connection error to {self.OLLAMA_URL}")
            print(f"   Make sure Ollama is running: ollama serve")
            return ""
        except requests.exceptions.Timeout:
            print(f"❌ Ollama request timed out at {self.OLLAMA_URL}")
            return ""
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return ""
