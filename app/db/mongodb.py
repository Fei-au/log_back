from motor import motor_asyncio
from pymongo import MongoClient
from app.core.config import settings

# MongoDB client setup
client = motor_asyncio.AsyncIOMotorClient(settings.mongodb_dsn)
sync_client = MongoClient(settings.mongodb_dsn)

db_bidLog = client.bidLog

db_traces = client.traces

db_refunds = client.refunds

sync_db_task_logs = sync_client.task_logs

# For Relational Database
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from app.core.config import settings

# SQLALCHEMY_DATABASE_URL = settings.database_url

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()