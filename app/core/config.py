from pydantic import MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Log Back"
    mongodb_dsn: str
    google_application_credentials: str

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()