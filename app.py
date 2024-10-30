from fastapi import FastAPI, HTTPException
from datetime import datetime
from db import db, LogModel, ItemLog
from typing import List

app = FastAPI()


@app.post("/items/logs")
async def create_item_logs(automation_link: str, client: str, items: List[ItemLog]):
    item_logs = [item.model_dump(by_alias=True) for item in items]
    for item in item_logs:
        item["automation_link"] = automation_link
        item["client"] = client
    try:
        result = await db.item_logs.insert_many(item_logs)
        item_log_ids = result.inserted_ids
        return {"status": "batch_inserted", "batch_size": len(item_log_ids), "item_log_ids": [str(id) for id in item_log_ids]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/logs/complete")
async def complete_log(client: str, automation_link: str, success: bool, cust_win_count: int, cust_win_increased_price: float, bot_win_count: int, bot_win_increased_price: float, message: str = None):
    try:
        log_entry = LogModel(
            timestamp=datetime.now(),
            client=client,
            automation_link=automation_link,
            action="Automated Pricing",
            success=success,
            cust_win_count=cust_win_count,
            cust_win_increased_price=cust_win_increased_price,
            bot_win_count=bot_win_count,
            bot_win_increased_price=bot_win_increased_price,
            message=message,
        )
        result = await db.logs.insert_one(log_entry.model_dump(by_alias=True))
        return {"status": "log_completed", "log_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))