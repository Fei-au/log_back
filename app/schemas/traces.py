from typing import Optional
from pydantic import BaseModel


class OrderItem(BaseModel):
    trace_id: str
    invoice_number: str
    order_id: Optional[str] = None
    item_number: str
    order_item_id: Optional[str] = None
    is_inputed: Optional[bool] = False
    is_ticked: Optional[bool] = False
    sold_time: str

    
    