from fastapi import FastAPI
from app.api.v1 import logs, traces
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from pathlib import Path
from strawberry.fastapi import GraphQLRouter
from app.graphql.schema import schema
from app.core.config import celery_app

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None
)

graphql_app = GraphQLRouter(schema)
    
origins = [
    "http://manage.ruitotrading.com",
    "https://manage.ruitotrading.com",
    "http://192.168.217.1:3001",
    "http://192.168.0.247:3001",
    "http://127.0.0.1:3001",
    "http://127.0.0.1",
]

BASE_DIR = Path(__file__).resolve().parent.parent

logging.basicConfig(
    level=logging.INFO,
    filename=os.path.join(BASE_DIR, "log_back_FastAPI.log"),
    filemode="a",
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Log Back API!"}

@app.get("/test")
async def test():
    celery_app.send_task('orders.tasks.test_success', args=[1,2,3])
    return {"message": "Test endpoint is working!"}

app.include_router(logs.router, prefix="/logs",  tags=["Logs"])
app.include_router(traces.router, prefix="/traces",  tags=["traces"])
app.include_router(graphql_app, prefix="/graphql",  tags=["graphql"])
