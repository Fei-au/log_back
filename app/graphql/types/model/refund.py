import strawberry
from typing import List, Optional

# mongodb order item model
@strawberry.type
class OrderItem:
    # order item id
    id: strawberry.ID
    # item id
    item_id: int
    item_number: str
    lot: str
    # price: Float!
    pure_price: float
    tax: float
    handling_fee: float
    premium_fee: float
    total_price: float
    refund_amount: float
    after_ordered_status: str
    other_status: Optional[str]
    pickup_time: Optional[str]
    sold_time: Optional[str]
    # complete: bool=False

# mongodb refund invoice model
@strawberry.type
class RefundInvoiceModel:
    # mongodb generated unique id
    _id: strawberry.ID
    # invoice_number + yymmdd + timestamp last four digit
    refund_id: str
    order_id: int
    invoice_number: str
    auction: int
    order_items: List[OrderItem]
    created_at: str
    has_completed: bool
    completed_time: Optional[str] = None
    total_refund_amount: float
    has_voided: bool
    voided_time: Optional[str] = None
    staff_user_id: int
    staff_name: str
    refund_invoice_path: Optional[str] = None
    problem_item_path: Optional[str] = None
