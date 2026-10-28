
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    postgres_password: str

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def database_url(self) -> str:
        from urllib.parse import quote

        password = quote(self.postgres_password, safe="")
        return (
            "postgresql+psycopg://documind_user:"
            f"{password}@127.0.0.1:5432/documind"
        )


settings = Settings()
