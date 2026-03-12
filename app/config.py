from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ResuMate"
    app_version: str = "1.0.0"
    api_prefix: str = "/v1"

    mongo_uri: Optional[str] = Field(default=None, alias="MONGO_URI")
    mongo_db_name: str = "resumate"
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
