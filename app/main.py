from fastapi import FastAPI
from app.api.v1 import logs, traces


app = FastAPI()
    
app.include_router(logs.router, prefix="/logs",  tags=["Logs"])
app.include_router(traces.router, prefix="/traces",  tags=["traces"])