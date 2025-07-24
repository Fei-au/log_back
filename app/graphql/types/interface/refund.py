import strawberry
from typing import List, Optional
from app.graphql.types.model.refund import OrderItem

@strawberry.interface
class RefundInvoiceBase:
    # mongodb generated unique id
    _id: strawberry.ID
    # invoice_number + yymmdd + timestamp last four digit
    refund_id: str
    order_id: int
    invoice_number: int
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
