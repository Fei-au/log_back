from typing import Optional, Union
from pydantic import BaseModel


class OrderItem(BaseModel):
    trace_id: str
    invoice_number: Union[str, int]  # str or int
    order_id:  int
    item_number: str
    order_item_id: Optional[int] = None
    is_scanned: Optional[bool] = False
    is_ticked: Optional[bool] = False
    is_in_invoice: bool
    sold_time: str
    note: Optional[str] = None

    
    