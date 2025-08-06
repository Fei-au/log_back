
from typing import Optional, List
from pydantic import  BaseModel
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    success = "success"
    failed = "failed"
    skip = "skip"

class ItemLog(BaseModel):
    transaction_id: Optional[str] = None
    automation_link: Optional[str] = None          # Link or unique identifier for the automation process
    lot: str                  # Unique identifier for each item (e.g., SKU or database ID)
    client: Optional[str] = None                   # Identifier for the client (e.g., username or user ID)
    target_price: float           # Final price automated to
    previous_price: Optional[float] = None  # (Optional) Original price before automation
    status: str                   # Status of automation, e.g., "success" or "skip"
    timestamp: datetime           # Time when this specific item was automated

    
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
    
class FilterBidderTxnsModel(BaseModel):
    transaction_id: str
    automation_link: str
    timestamp: datetime
    client: Optional[str] = None
    status: Status
    checked_bidder_count: int
    blocked_bidder_count: int
    message: Optional[str] = None
    
class LogBidderBlockModel(BaseModel):
    transaction_id: Optional[str] = None
    automation_link: Optional[str] = None   # Link or unique identifier for the automation process
    timestamp: datetime # Time when this specific item was automated
    client: Optional[str] = None    # Identifier for the client (e.g., username or user ID)
    bidder_id: str  # blocked user id
    status: Status # Status of automation, e.g., "success" -> block success or "failed" block failed
    message: Optional[str] = None
    
    