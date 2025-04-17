from fastapi import FastAPI
from app.api.v1 import logs, traces
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
    
origins = [
    "http://manage.ruitotrading.com",
    "https://manage.ruitotrading.com",
    "http://192.168.217.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(logs.router, prefix="/logs",  tags=["Logs"])
app.include_router(traces.router, prefix="/traces",  tags=["traces"])