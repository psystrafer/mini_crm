from pydantic_settings import SettingsConfigDict, BaseSettings
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.getenv("CRM_ENV", "./.env"),
        env_file_encoding="utf-8",
    )

    db_dsn: str
    root_path: str = "/api/v1"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 1
    REFRESH_TOKEN_EXPIRE_DAYS: int = 5


settings = Settings()
