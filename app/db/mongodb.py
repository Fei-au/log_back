import motor.motor_asyncio
from app.core.config import settings

# MongoDB client setup
client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongodb_dsn)

db_bidLog = client.bidLog

db_traces = client.traces



# For Relational Database
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from app.core.config import settings

# SQLALCHEMY_DATABASE_URL = settings.database_url

# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()