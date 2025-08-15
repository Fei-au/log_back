from pydantic import MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from celery import Celery


class Settings(BaseSettings):
    app_name: str = "Log Back"
    mongodb_dsn: str
    google_application_credentials: str
    # media_dir: str
    # media_host: str
    broker_url: str
    
    model_config = SettingsConfigDict(env_file='.env')
    
settings = Settings()

# Celery app initalize, used for publishing messages
celery_app = Celery(
    'celery',
    broker=settings.broker_url,
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='America/Toronto',
    enable_utc=True,
)