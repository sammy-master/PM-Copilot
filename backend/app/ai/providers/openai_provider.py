"""
PM Copilot - OpenAI Provider
------------------------------
Implements the AIProvider interface for OpenAI's cloud models.
Used as a fallback or when better quality is needed.
"""

from typing import AsyncGenerator

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.ai.providers.base import AIProvider
from app.config import settings


class OpenAIProvider(AIProvider):
    """AI Provider that uses OpenAI's API (GPT-4o-mini, GPT-4o, etc.)"""

    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=0.7,
            streaming=True,
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
