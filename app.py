from fastapi import FastAPI, HTTPException
from datetime import datetime
from db import db, LogModel, ItemLog, ItemLogRequest
from typing import List

app = FastAPI()


@app.post("/logs/items")
async def create_item_logs(log_request: ItemLogRequest):
    try:
        items = log_request.items
        automation_link = log_request.automation_link
        client = log_request.client
        transaction_id = log_request.transaction_id
        for item in items:
            item.transaction_id = transaction_id
            item.automation_link = automation_link
            item.client = client
        result = await db.bids.insert_many([item.model_dump() for item in items])
        items_ids = result.inserted_ids
        return {"status": "batch_inserted", "batch_size": len(items_ids), "item_log_ids": [str(id) for id in items_ids]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/logs/transaction")
async def complete_log(log_complete: LogModel):
    try:
        result = await db.transactions.insert_one(log_complete.model_dump())
        return {"status": "transaction_completed", "log_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))