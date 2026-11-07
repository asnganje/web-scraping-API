from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    app_name:str
    debug:bool = True
    database_url:str

    model_config = SettingsConfigDict(env_file=PROJECT_ROOT / ".env")

settings = Settings()