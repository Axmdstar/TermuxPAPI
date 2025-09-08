from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "My FastAPI Application"
    VERSION: str = "1.0.0"
    API_V: str = "/api/v1"
    DATABASE_URL: Optional[str] = None

    BACKEND_CORS_ORIGINS: list = ["*"]

    class Config:
        env_file = ".env"


settings = Settings()
