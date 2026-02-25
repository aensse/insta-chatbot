from pathlib import Path

from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    xai_api_key: SecretStr
    ig_username: str
    ig_password: str
    ig_secret: str | None = None

    grok_model: str = "grok-4-1-fast-non-reasoning"

    db_name: str = "threads.db"

    @property
    def db_url(self):
        return f"sqlite+aiosqlite:///./{self.db_name}"



class Files(BaseSettings):
    instructions_file: Path = Path.cwd() / "instructions.txt"
    session_file: Path = Path.cwd() / "ig_session.json"
    mqtt_file: Path = Path.cwd() / "mqtt_process.js"

    @computed_field
    @property
    def get_instructions(self) -> str:
        if not self.instructions_file.exists():
            raise ValueError("Instructions for AI does not exist")
        with self.instructions_file.open("r", encoding="utf-8") as f:
            return f.read()


settings = Settings()
files = Files()

