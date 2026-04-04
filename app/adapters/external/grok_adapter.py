from typing import Annotated, Literal

from pydantic import BaseModel, Field
from xai_sdk import AsyncClient
from xai_sdk.chat import assistant, system, user

from app.domain.models import InstagramThread, LLMResponse


class ThreadInfo(BaseModel):
    message: Annotated[
        str,
        Field(
            description="Message to the user based on the context of the entire conversation."  # noqa: E501
        ),
    ]
    status: Annotated[
        Literal["active", "blocked"],
        Field(
            description="User status based on instructions from the beginning of the conversation."  # noqa: E501
        ),
    ]


class GrokLLMAdapter:
    def __init__(self, cl: AsyncClient, model: str, instructions: str) -> None:
        self.cl = cl
        self.model = model
        self.instructions = instructions

    async def get_ai_response(self, thread: list[InstagramThread]) -> ThreadInfo:
        chat = self.cl.chat.create(model=self.model)
        chat.append(system(self.instructions))

        for message in thread:
            if message.is_sent_by_viewer:
                chat.append(assistant(message.text)) if message.text else None
            else:
                chat.append(user(message.text)) if message.text else None

        _, user_info = await chat.parse(ThreadInfo)
        return LLMResponse(**user_info.model_dump())
