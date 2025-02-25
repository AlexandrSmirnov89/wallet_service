from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from environs import Env


env = Env()
env.read_env()

class Settings(BaseSettings):
    DATABASE_URL: str = env('DATABASE_URL')
    REDIS_URL: str = env('REDIS_URL')
    model_config = ConfigDict(env_file=".env")


settings = Settings()
