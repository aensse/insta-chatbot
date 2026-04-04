from typing import Any, Protocol

from app.domain.models import LLMResponse


class LLMPort(Protocol):
    async def get_ai_response(self, thread: list[Any]) -> LLMResponse: ...
