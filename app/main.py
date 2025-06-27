from fastapi import FastAPI
from app.api.v1 import logs, traces
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from pathlib import Path

app = FastAPI()
    
origins = [
    "http://manage.ruitotrading.com",
    "https://manage.ruitotrading.com",
    "http://192.168.217.1:3001",
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

app.include_router(logs.router, prefix="/logs",  tags=["Logs"])
app.include_router(traces.router, prefix="/traces",  tags=["traces"])