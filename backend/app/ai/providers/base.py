"""
PM Copilot - AI Provider Abstraction (Base Interface)
------------------------------------------------------
WHY THIS EXISTS:
  This is the most important AI design decision in this project.
  
  Instead of hardcoding "use Ollama" or "use OpenAI" everywhere,
  we define a common interface that ALL providers must follow.
  
  This means:
    - The rest of the app calls: ai_provider.generate(prompt)
    - You switch models by changing ONE env variable: AI_PROVIDER=openai
    - Adding a new provider = just implement this interface
  
  This demonstrates the "Dependency Inversion" principle from SOLID —
  your app depends on an abstraction, not a specific implementation.

VIVA EXPLANATION:
  "I designed the AI layer as a provider pattern. All LLM providers —
   Ollama, OpenAI, Gemini — implement the same interface. The application
   only talks to the interface, so switching models requires changing
   just one environment variable."
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator


class AIProvider(ABC):
    """
    Abstract base class for all LLM providers.
    Every provider (Ollama, OpenAI, Gemini) must implement these methods.
    """

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        Generate a complete response from the LLM.

        Args:
            prompt: The user's input / instruction
            system_prompt: Sets the AI's persona and behavior

        Returns:
            The complete generated text as a string
        """
        pass

    @abstractmethod
    async def stream(
        self, prompt: str, system_prompt: str = ""
    ) -> AsyncGenerator[str, None]:
        """
        Stream the LLM response token by token.
        Used for the typewriter effect in the chat UI.

        Args:
            prompt: The user's input
            system_prompt: Sets the AI's persona

        Yields:
            Individual text tokens/chunks as they are generated
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the provider is reachable and working.
        Returns True if healthy, False otherwise.
        """
        pass
