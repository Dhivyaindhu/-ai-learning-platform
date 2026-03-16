# ai_engine/llm/client.py
# OLLAMA BACKEND: Uses local qwen-local model via Ollama server

import requests


class LocalLLM:

    DEFAULT_SYSTEM = (
        "You are a helpful assistant for an AI-powered learning platform. "
        "Follow instructions exactly and be concise."
    )

    OLLAMA_URL  = "http://localhost:11434/api/generate"
    OLLAMA_BASE = "http://localhost:11434"

    def __init__(self, model_name="qwen-local"):
        self.model_name = model_name
        print(f"🔄 Initializing Ollama client...")

        try:
            requests.get(self.OLLAMA_BASE, timeout=5)
            print(f"✅ Ollama server: running")
            print(f"✅ Model: {model_name}")
        except Exception:
            print(f"❌ Ollama server not running!")
            print(f"   Open a terminal and run: ollama serve")

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
                    "num_ctx":        1024,   # increased from 512 to fix truncation
                }
            }

            response = requests.post(
                self.OLLAMA_URL,
                json=payload,
                timeout=120,
            )
            response.raise_for_status()
            result = response.json().get("response", "").strip()
            return result if result else ""

        except requests.exceptions.ConnectionError:
            print(f"❌ Ollama not running. Open terminal and run: ollama serve")
            return ""
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return ""