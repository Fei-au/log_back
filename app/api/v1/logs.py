from fastapi import HTTPException, APIRouter
from app.schemas.logs import ItemLogRequest, LogModel, ItemLogResponse, LogResponse
from app.crud.logs import insert_bids, insert_transaction


router = APIRouter()

@router.post("/items", response_model=ItemLogResponse)
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
        inserted_ids = await insert_bids([item.model_dump() for item in items])
        return {"status": "batch_inserted", "batch_size": len(inserted_ids), "item_log_ids": [str(id) for id in inserted_ids]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transaction", response_model=LogResponse)
async def complete_log(log_complete: LogModel):
    try:
        inserted_id = await insert_transaction(log_complete.model_dump())
        return {"status": "transaction_completed", "log_id": str(inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))