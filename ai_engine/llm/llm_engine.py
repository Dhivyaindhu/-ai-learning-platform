# ai_engine/llm/llm_engine.py
import time, re, os, sys
from typing import Dict, Any

_llm_instance = None

def get_llm_engine():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = LLMEngine()
    return _llm_instance

def _should_skip_init():
    build_commands = {
        "collectstatic", "migrate", "makemigrations",
        "check", "shell", "createsuperuser"
    }
    for cmd in build_commands:
        if cmd in sys.argv:
            print(f"🔧 LLM Engine: skipping init during '{cmd}' command")
            return True
    return False

class LLMEngine:

    def __init__(self):
        self.llm_client             = None
        self.use_real_model         = False
        self.model_name             = None
        self.generation_count       = 0
        self.success_count          = 0
        self.error_count            = 0
        self.total_tokens_generated = 0

        if _should_skip_init():
            return

        print("🚀 LLM Engine: INITIALIZING...")
        self._initialize_model()

    def _initialize_model(self):
        try:
            print("🔧 Initializing LLM Engine (Ollama)...")
            from .client import LocalLLM

            self.llm_client = LocalLLM(model_name="qwen-local")

            if self.llm_client._connected:
                print("   Testing generation...")
                test = self.llm_client.generate(
                    "Say hello in 3 words.", max_tokens=10
                )
                if test:
                    self.use_real_model = True
                    self.model_name     = "qwen-local"
                    print(f"✅ LLM ready: qwen-local via Ollama")
                    print(f"   Test output: '{test}'")
                else:
                    print("⚠️  Ollama reachable but empty response")
                    self.use_real_model = True
                    self.model_name     = "qwen-local"
            else:
                # Not connected at startup — still allow retries on generate()
                print("⚠️  Ollama not reachable at startup")
                print("   Will retry automatically on each LLM call")
                self.use_real_model = True
                self.model_name     = "qwen-local"

        except Exception as e:
            print(f"⚠️  LLM init error: {e}")
            self.use_real_model = False

    def generate(self, prompt, max_length=150, max_tokens=None,
                 retries=2, system_prompt=None):
        tokens_to_use = max_tokens if max_tokens is not None else max_length
        self.generation_count += 1

        if not self.llm_client:
            self.error_count += 1
            return ""

        for attempt in range(retries + 1):
            try:
                if attempt:
                    print(f"      Retry {attempt}/{retries}...")

                raw = self.llm_client.generate(
                    prompt=prompt,
                    max_tokens=tokens_to_use,
                    system_prompt=system_prompt,
                )
                cleaned = self._clean(raw)

                if len(cleaned) >= 10:
                    self.use_real_model         = True
                    self.success_count          += 1
                    self.total_tokens_generated += len(cleaned.split())
                    return cleaned

                if attempt < retries:
                    time.sleep(0.3)

            except TypeError as e:
                print(f"   ❌ TypeError: {e}")
                self.error_count += 1
                return ""
            except Exception as e:
                print(f"   ❌ Error (attempt {attempt+1}): {e}")
                if attempt < retries:
                    time.sleep(1)

        self.error_count += 1
        return ""

    def generate_long_content(self, prompt, max_tokens=1500, retries=3):
        print(f"   📝 Long generation ({max_tokens} tokens)...")
        result = self.generate(prompt, max_length=max_tokens, retries=retries)
        if result:
            print(f"   ✅ {len(result)} chars generated")
        else:
            print("   ❌ Long generation failed — using fallback content")
        return result

    def _clean(self, text):
        if not text: return ""
        t = text.strip()
        prefixes = (
            "sure!","sure,","sure.","here's one for you:","here's one for you",
            "here's a question:","here's","here is","okay,","ok,","alright,",
            "let me","i'll","i will","certainly,","of course","great!","great,",
            "sure thing","absolutely,","no problem,",
        )
        for p in prefixes:
            if t.lower().startswith(p):
                t = t[len(p):].lstrip(" ,:.!")
                break
        t = re.sub(r' {2,}', ' ', t)
        if t and t[-1] not in '.!?':
            for p in ['.','!','?']:
                idx = t.rfind(p)
                if idx > len(t)*0.5:
                    t = t[:idx+1]
                    break
        return t.strip()

    def get_stats(self):
        total = self.generation_count
        return {
            "total":        total,
            "success":      self.success_count,
            "failed":       self.error_count,
            "success_rate": round(self.success_count/total*100, 1) if total else 0,
            "total_tokens": self.total_tokens_generated,
            "model_loaded": self.use_real_model,
            "model_name":   self.model_name or "None",
        }

    def generate_text(self, prompt, max_tokens=150):
        return self.generate(prompt, max_length=max_tokens)

    def generate_structured(self, prompt, max_length=150):
        return self.generate(prompt, max_length=max_length, retries=1)
