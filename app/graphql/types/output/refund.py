import strawberry
from typing import Optional, List
from app.graphql.types.model.refund import OrderItem
from app.tools.gcp_tools import generate_signed_url

@strawberry.type
class RefundInvoiceCreateOutput:
    signed_refund_path: str
    signed_problem_item_path: str
    inserted_id: str

@strawberry.type
class RefundInvoiceQueryOutput:

    # mongodb generated unique id
    _id: strawberry.ID
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

    @strawberry.field
    def signed_refund_invoice_path(self) -> Optional[str]:
        # Logic to generate signed URL for refund_invoice_path
        return generate_signed_url(self.refund_invoice_path)

    @strawberry.field
    def signed_problem_item_path(self) -> Optional[str]:
        # Logic to generate signed URL for problem_item_path
        return generate_signed_url(self.problem_item_path)
