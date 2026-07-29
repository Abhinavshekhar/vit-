from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AstraOS"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://astra:astra@localhost:5432/astraos"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "change-me"
    openai_api_key: str | None = None
    encryption_key_base64: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
