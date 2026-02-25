from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


class UserMessage(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    message: Annotated[str, Field(min_length=2, max_length=1000)]
    user: Annotated[str | None, Field(default=None, min_length=3, max_length=50)]

    action_params: Annotated[dict, Field(alias="actionParams")]
    category: Annotated[str, Field(alias="pushCategory", min_length=1, max_length=100)]

    user_id: Annotated[int, Field(alias="sourceUserId")]

    @model_validator(mode="after")
    def extract_user(self):
        parts = self.message.split(":", 1)
        if len(parts) < 2:  # noqa: PLR2004
            raise ValueError("Invalid message format")
        self.user = parts[0]
        self.message = parts[1].replace(" ", "", 1)
        return self

    @computed_field
    @property
    def thread_id(self) -> str:
        thread_id = self.action_params.get("id")
        if not thread_id:
            raise ValueError("Missing thread ID data.")
        return thread_id


class BotResponse(BaseModel):
    user: str
    status: str
    message_to_user: str
