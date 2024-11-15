import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=os.getenv("ENV_FILE_PATH"), env_file_encoding="utf-8"
    )

    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int

    AUTH_COOKIE_HTTPONLY: bool
    AUTH_COOKIE_SECURE: bool
    AUTH_COOKIE_SAME_SITE: Literal["lax", "none", "strict"]

    LOG_AWS_ACCESS_KEY: str
    LOG_AWS_SECRET_ACCESS_KEY: str

    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


conf = Config()
