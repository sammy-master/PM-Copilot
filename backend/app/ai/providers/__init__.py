"""
PM Copilot - AI Provider Factory
----------------------------------
The factory function reads the AI_PROVIDER environment variable
and returns the correct provider instance.

This is the ONLY place in the codebase that knows which provider is active.
Everything else just uses the AIProvider interface.

VIVA EXPLANATION:
  "This is the Factory pattern. Based on one environment variable,
   the entire AI layer switches providers. The rest of the application
   doesn't know or care which LLM is being used."
"""

from app.config import settings
from app.ai.providers.base import AIProvider


def get_ai_provider() -> AIProvider:
    """
    Factory function — returns the correct AI provider based on config.

    Usage:
        provider = get_ai_provider()
        response = await provider.generate("Write a PRD for...")
    """
    provider_name = settings.ai_provider.lower()

    if provider_name == "ollama":
        from app.ai.providers.ollama_provider import OllamaProvider
        return OllamaProvider()

    elif provider_name == "openai":
        from app.ai.providers.openai_provider import OpenAIProvider
        return OpenAIProvider()

    elif provider_name == "gemini":
        from app.ai.providers.gemini_provider import GeminiProvider
        return GeminiProvider()

    else:
        raise ValueError(
            f"Unknown AI provider: '{provider_name}'. "
            f"Valid options: 'ollama', 'openai', 'gemini'"
        )


# Singleton — create once and reuse across the application
ai_provider: AIProvider = get_ai_provider()
