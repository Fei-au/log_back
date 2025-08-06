
from typing import List
from pydantic import BaseModel
from app.models.logs import ItemLog

class ItemLogRequest(BaseModel):
    transaction_id: str
    items: List[ItemLog]
    automation_link: str
    client: str
    
class ItemLogResponse(BaseModel):
    status: str
    batch_size: int
    item_log_ids: List[str]

class LogResponse(BaseModel):
    status: str
    log_id: str

# class ErrorLogModel(BaseModel):