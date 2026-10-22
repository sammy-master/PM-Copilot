"""
PM Copilot - Gemini Provider
------------------------------
Implements the AIProvider interface for Google's Gemini models.
"""

from typing import AsyncGenerator

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.ai.providers.base import AIProvider
from app.config import settings


class GeminiProvider(AIProvider):
    """AI Provider that uses Google's Gemini API."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            google_api_key=settings.gemini_api_key,
            temperature=0.7,
        )

    async def generate(self, prompt: str, system_prompt: str = "") -> str:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))
        response = await self.llm.ainvoke(messages)
        return response.content

    async def stream(
        self, prompt: str, system_prompt: str = ""
    ) -> AsyncGenerator[str, None]:
        messages = []
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=prompt))

        async for chunk in self.llm.astream(messages):
            if chunk.content:
                yield chunk.content

    async def health_check(self) -> bool:
        try:
            response = await self.llm.ainvoke([HumanMessage(content="ping")])
            return bool(response.content)
        except Exception:
            return False
