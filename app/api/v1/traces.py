from fastapi import APIRouter
from app.schemas.base import ResponseBase, InsertOneResponse
from app.models.traces import OrderItem
from app.crud.traces import insert_order_item


router = APIRouter()

@router.post("/order_item/", response_model=ResponseBase[InsertOneResponse], response_description="Order Item")
async def order_item(order_item: OrderItem):
    inserted_id = await insert_order_item(order_item)
    return ResponseBase(data=InsertOneResponse(inserted_id=inserted_id))

