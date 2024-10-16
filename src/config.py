from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file="../.env", env_file_encoding="utf-8")

    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str

    @property
    def DB_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


conf = Config()
