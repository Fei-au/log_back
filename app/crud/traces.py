from app.db.mongodb import db_traces
from app.schemas.traces import OrderItem


async def insert_order_item(order_item: OrderItem):
    result = await db_traces.bids.insert_one(order_item.model_dump())
    return str(result.inserted_id)