
from typing import Optional, List
from pydantic import  BaseModel
from datetime import datetime


class ItemLog(BaseModel):
    transaction_id: Optional[str] = None
    automation_link: Optional[str] = None          # Link or unique identifier for the automation process
    lot: str                  # Unique identifier for each item (e.g., SKU or database ID)
    client: Optional[str] = None                   # Identifier for the client (e.g., username or user ID)
    target_price: float           # Final price automated to
    previous_price: Optional[float] = None  # (Optional) Original price before automation
    status: str                   # Status of automation, e.g., "Success" or "Failed"
    timestamp: datetime           # Time when this specific item was automated

class ItemLogRequest(BaseModel):
    transaction_id: str
    items: List[ItemLog]
    automation_link: str
    client: str
    
class ItemLogResponse(BaseModel):
    status: str
    batch_size: int
    item_log_ids: List[str]
    
class LogModel(BaseModel):
    transaction_id: str
    automation_link: str          # Link or unique identifier for the automation process
    timestamp: datetime           # Main timestamp for the logging event
    client: Optional[str] = None  # Identifier for the client (e.g., username or user ID)
    action: str                   # Description of action, e.g., "Automated Pricing"
    # items: List[ItemLog]          # List of items automated, using the ItemLog structure
    success: bool                 # Status of the overall automation process (True for success, False for failure)
    message: Optional[str] = None # Optional field for additional notes or error messages if the process fails
    cust_win_count: int
    cust_win_increased_price: float
    bot_win_count: int
    bot_win_increased_price: float
    
class LogResponse(BaseModel):
    status: str
    log_id: str
    
# class ErrorLogModel(BaseModel):