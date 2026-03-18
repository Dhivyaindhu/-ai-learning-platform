# ai_engine/llm/client.py
# OLLAMA BACKEND: Uses local qwen-local model via Ollama server

import requests
import os


class LocalLLM:

    DEFAULT_SYSTEM = (
        "You are a helpful assistant for an AI-powered learning platform. "
        "Follow instructions exactly and be concise."
    )

    # GET URL FROM ENVIRONMENT VARIABLE!
    OLLAMA_BASE = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_URL  = f"{OLLAMA_BASE}/api/generate"

    def __init__(self, model_name="qwen-local"):
        self.model_name = model_name
        print(f"🔄 Initializing Ollama client...")
        print(f"🔗 Ollama URL: {self.OLLAMA_BASE}")  # DEBUG: Show which URL we're using

        try:
            requests.get(self.OLLAMA_BASE, timeout=5)
            print(f"✅ Ollama server: running")
            print(f"✅ Model: {model_name}")
        except Exception as e:
            print(f"❌ Ollama server not running!")
            print(f"   URL: {self.OLLAMA_BASE}")
            print(f"   Error: {e}")

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

            print(f"🔍 Calling Ollama at: {self.OLLAMA_URL}")  # DEBUG
            
            response = requests.post(
                self.OLLAMA_URL,
                json=payload,
                timeout=120,
            )
            
            print(f"🔍 Response status: {response.status_code}")  # DEBUG
            
            response.raise_for_status()
            result = response.json().get("response", "").strip()
            
            print(f"🔍 Generated text length: {len(result)}")  # DEBUG
            
            return result if result else ""

        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection error to {self.OLLAMA_URL}: {e}")
            return ""
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return ""
