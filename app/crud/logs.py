from app.db.mongodb import db_bidLog
from app.schemas.logs import ItemLog, LogModel, FilterBidderTxnsModel, LogBidderBlockModel


async def insert_bid(item: ItemLog):
    result = await db_bidLog.bids.insert_one(item.model_dump())
    return result.inserted_id

async def insert_bids(items: list[ItemLog]):
    result = await db_bidLog.bids.insert_many([item.model_dump() for item in items])
    return result.inserted_ids

async def insert_transaction(log_complete: LogModel):
    result = await db_bidLog.transactions.insert_one(log_complete.model_dump())
    return result.inserted_id

async def insert_filter_txn(filter_txn: FilterBidderTxnsModel):
    result = await db_bidLog.filter_txn.insert_one(filter_txn.model_dump())
    return str(result.inserted_id)

async def insert_block_bidder(block_bidder_log: LogBidderBlockModel):
    result = await db_bidLog.filter_block.insert_one(block_bidder_log.model_dump())
    return str(result.inserted_id)