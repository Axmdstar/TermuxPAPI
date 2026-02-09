# from typing import

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My FastAPI Application"
    VERSION: str = "1.0.0"
    API_V1: str = "/api/v1"
    DATABASE_URL: str | None = None

    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
