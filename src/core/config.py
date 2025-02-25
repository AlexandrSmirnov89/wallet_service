from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://wallet_admin:qwerty@db:5432/wallet_service"
    REDIS_URL: str = "redis://redis:6379/0"
    model_config = ConfigDict(env_file=".env")


settings = Settings()
