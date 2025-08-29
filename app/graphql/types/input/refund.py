import strawberry
from typing import List, Optional

@strawberry.input
class QueryInput:
    invoice_number: Optional[str] = None
    has_completed: Optional[bool] = None
    has_voided: Optional[bool] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    
@strawberry.input
class ExportCsvInput:
    ids: List[str]
        

@strawberry.input
class OrderItemInput:
    # Order item id
    id: int
    # Item id
    item_id: int
    item_number: str
    lot: str
    pure_price: float
    tax: Optional[float] = None
    handling_fee: Optional[float] = None
    premium_fee: Optional[float] = None
    total_price: float
    refund_amount: float
    after_ordered_status: str
    other_status: Optional[str] = None
    pickup_time: Optional[str] = None
    sold_time: Optional[str] = None
    # complete: bool = False

@strawberry.input
class RefundInvoiceCreateInput:
    # order id
    order_id: int
    invoice_number: str
    auction: int
    has_completed: bool
    order_items: List[OrderItemInput]
    total_refund_amount: float
    staff_user_id: int
    staff_name: str
    is_store_credit: bool
    refund_email: Optional[str] = None

@strawberry.input
class VoidRefundInvoiceInput:
    refund_id: str
    
@strawberry.input
class CompleteRefundInvoiceInput:
    refund_id: str
