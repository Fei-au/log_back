from fastapi import HTTPException, APIRouter
from app.schemas.logs import ItemLogRequest, ItemLogResponse, LogResponse
from app.models.logs import LogModel, FilterBidderTxnsModel, LogBidderBlockModel
from app.crud.logs import insert_bids, insert_transaction, insert_filter_txn, insert_block_bidder
import logging
from app.schemas.base import ResponseBase, InsertOneResponse


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
        return {"status": "success", "batch_size": len(inserted_ids), "item_log_ids": [str(id) for id in inserted_ids]}
    except Exception as e:
        logger.error(f"Failed to insert items: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transaction", response_model=LogResponse)
async def complete_log(log_complete: LogModel):
    try:
        inserted_id = await insert_transaction(log_complete)
        return {"status": "success", "log_id": str(inserted_id)}
    except Exception as e:
        logger.error(f"Failed to insert transaction log: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/block_bidder_log/", response_model=ResponseBase[InsertOneResponse])
async def block_bidder_log(block_bidder_log: LogBidderBlockModel):
    try:
        inserted_id = await insert_block_bidder(block_bidder_log)
        return ResponseBase(data=InsertOneResponse(inserted_id=inserted_id))
    except Exception as e:
        logger.error(f"Failed to insert bidder block log: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/filter_bidder_txns/", response_model=ResponseBase[InsertOneResponse])
async def add_filter_bidder_txns(filter_txn: FilterBidderTxnsModel):
    try:
        inserted_id = await insert_filter_txn(filter_txn)
        return ResponseBase(data=InsertOneResponse(inserted_id=inserted_id))
    except Exception as e:
        logger.error(f"Failed to insert bidder transaction filter: {e}")
        raise HTTPException(status_code=500, detail=str(e))