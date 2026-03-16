from django.apps import AppConfig


class AiEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_engine'

    def ready(self):
        """
        Called once when Django starts.
        Pre-loads the LLM into memory so the first request isn't slow.
        """
        try:
            from .llm.llm_engine import get_llm_engine
            get_llm_engine()
        except Exception as e:
            print(f"⚠️  LLM preload skipped: {e}")