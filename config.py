# config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # This variable will automatically pull from OS environment,
    # and fall back to the .env file locally.
    DATABASE_URL: str

    # Configuration to load the .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    # Caches the settings object so it's loaded only once.
    return Settings()

# Optional: You can export the object directly
settings = get_settings()