from typing import Annotated

from aiograpi.types import DirectMessage
from pydantic import BaseModel, Field
from xai_sdk import AsyncClient
from xai_sdk.chat import assistant, system, user

from app.infrastructure.models import ThreadStatus


class UserInfo(BaseModel):
    message: Annotated[str, Field(description="Message to the user based on the context of the entire conversation.")]
    status: Annotated[
        ThreadStatus, Field(description="User status based on instructions from the beginning of the conversation.")
    ]


class GrokClient:
    def __init__(self, api_key: str, model: str, instructions: str) -> None:
        self.api_key = api_key
        self.model = model
        self.instructions = instructions

    async def get_ai_response(self, thread: list[DirectMessage]) -> UserInfo:
        ai = AsyncClient(api_key=self.api_key)
        chat = ai.chat.create(model=self.model)
        chat.append(system(self.instructions))

        for message in thread:
            if message.is_sent_by_viewer:
                chat.append(assistant(message.text)) if message.text else None
            else:
                chat.append(user(message.text)) if message.text else None

        _, user_info = await chat.parse(UserInfo)
        return user_info






