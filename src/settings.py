from pydantic_settings import SettingsConfigDict, BaseSettings
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("CRM_ENV", "./.env"),
        env_file_encoding="utf-8",
    )

    db_dsn: str


settings = Settings()
