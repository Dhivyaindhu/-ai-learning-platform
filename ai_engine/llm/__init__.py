# ai_engine/llm/__init__.py

from .client import LocalLLM
from .prompts import CAREER_FIT_ANALYSIS_PROMPT
from .llm_engine import LLMEngine
__all__ = ['LocalLLM', 'CAREER_FIT_ANALYSIS_PROMPT', 'LLMEngine']