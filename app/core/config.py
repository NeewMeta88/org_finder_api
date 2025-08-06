from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    DATABASE_URL: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = ConfigDict(
        env_file=".env",
    )

settings = Settings()