from app.db.mongodb import db_bidLog
from app.schemas.logs import ItemLog, LogModel


async def insert_bid(item: ItemLog):
    result = await db_bidLog.bids.insert_one(item.model_dump())
    return result.inserted_id

async def insert_bids(items: list[ItemLog]):
    result = await db_bidLog.bids.insert_many([item.model_dump() for item in items])
    return result.inserted_ids

async def insert_transaction(log_complete: LogModel):
    result = await db_bidLog.transactions.insert_one(log_complete.model_dump())
    return result.inserted_id