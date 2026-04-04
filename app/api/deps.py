from functools import cache
from pathlib import Path

from fastapi import BackgroundTasks, HTTPException, Query, Request, status
from xai_sdk import AsyncClient

from app.adapters.db.repositories.user_repository import UsersDB
from app.adapters.db.session import AsyncSessionLocal
from app.adapters.external.grok_adapter import GrokLLMAdapter
from app.adapters.external.instagram.aiograpi_adapter import AiograpiAdapter
from app.core.config import settings
from app.ports.llm_port import LLMPort


async def get_users_db():
    session = AsyncSessionLocal()
    try:
        yield UsersDB(session)
    finally:
        await session.close()


@cache
def get_instructions(file: Path = settings.ai_instructions_file) -> str:
    if not file.exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Instructions for AI does not exist",
        )
    with file.open("r", encoding="utf-8") as f:
        return f.read()


def get_aiograpi_adapter(request: Request) -> AiograpiAdapter:
    return request.app.state.aiograpi


def get_grok_adapter() -> GrokLLMAdapter:
    return GrokLLMAdapter(
        cl=AsyncClient(api_key=settings.llm_api_key.get_secret_value()),
        model=settings.llm_model,
        instructions=get_instructions(),
    )


LLM_ADAPTERS = {"grok": get_grok_adapter}


def get_llm_adapter(
    adapter_name: str = Query("grok", alias="llm_adapter"),
) -> LLMPort:
    adapter = LLM_ADAPTERS.get(adapter_name)
    if not adapter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported adapter"
        )
    return adapter()


def get_background_tasks(background_tasks: BackgroundTasks) -> BackgroundTasks:
    return background_tasks
