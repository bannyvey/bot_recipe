from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    admins_chat_id: int | None = None
    bot_token: str

    log_level: str = "DEBUG"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    host: str = "127.0.0.1"
    port: int = 8000
    backend_url: str = f"http://{host}:{port}"

    public_base_url: str | None = None
    webhook_secret: str = "change_me_for_webhook"

    page_size: int = 5

    model_config = SettingsConfigDict(
        env_file="../.env",
        extra="ignore",
    )


settings = Settings()
