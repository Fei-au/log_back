from fastapi import HTTPException, APIRouter
from app.schemas.logs import ItemLogRequest, LogModel, ItemLogResponse, LogResponse
from app.crud.logs import insert_bids, insert_transaction
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/items", response_model=ItemLogResponse)
async def create_item_logs(log_request: ItemLogRequest):
    try:
        items = log_request.items
        automation_link = log_request.automation_link
        client = log_request.client
        transaction_id = log_request.transaction_id
        
        updated_items = []
        for item in items:
            # Create a new ItemLog instance with updated fields
            updated_item = item.model_copy(update={
                "transaction_id": transaction_id,
                "automation_link": automation_link,
                "client": client
            })
            updated_items.append(updated_item)
        inserted_ids = await insert_bids(updated_items)
        return {"status": "batch_inserted", "batch_size": len(inserted_ids), "item_log_ids": [str(id) for id in inserted_ids]}
    except Exception as e:
        logger.error(f"Error inserting items: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transaction", response_model=LogResponse)
async def complete_log(log_complete: LogModel):
    try:
        inserted_id = await insert_transaction(log_complete)
        return {"status": "transaction_completed", "log_id": str(inserted_id)}
    except Exception as e:
        logger.error(f"Error inserting transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))