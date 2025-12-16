import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_name: str
    db_password: str
    db_user: str
    db_host: str
    db_port: str


    bot_token: str

    admins_chat_id: int | None = None

    log_level: str = "DEBUG"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    host: str = "localhost"
    port: int = 8000
    backend_url: str = f"http://{host}:{port}"

    webhook_url: str | None = None
    webhook_secret: str | None = None

    page_size: int = 5

    swagger_user: str
    swagger_password: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(Path(__file__).parent, ".env"),
        extra="ignore",
    )

    def create_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
