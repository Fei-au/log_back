import strawberry
from typing import List, Optional
from app.tools.gcp_tools import generate_signed_url

'''
Strawberry GraphQL, by default, automatically converts snake_case field names in Python 
to camelCase in the GraphQL schema. This is a common convention in GraphQL.
'''

@strawberry.input
class OrderItemInput:
    # Order item id
    id: int
    # Item id
    item_id: int
    item_number: str
    lot: str
    pure_price: float
    tax: float
    handling_fee: float
    premium_fee: float
    total_price: float
    refund_amount: float
    after_ordered_status: str
    other_status: Optional[str] = None
    pickup_time: Optional[str] = None
    sold_time: Optional[str] = None
    complete: bool = False

@strawberry.input
class RefundInvoiceCreateInput:
    # order id
    order_id: int
    invoice_number: int
    auction: int
    order_items: List[OrderItemInput]
    total_refund_amount: float
    staff_user_id: int
    staff_name: str

@strawberry.type
class RefundInvoiceCreateOutput:
    signed_refund_path: str
    signed_problem_item_path: str
    inserted_id: str

    
@strawberry.input
class voidRefundInvoiceInput:
    refund_id: str
    has_voided: bool
    
@strawberry.input
class CompleteRefundInvoiceInput:
    refund_id: str
    has_completed: bool

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
    complete: bool=False

# mongodb refund invoice model
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
    
@strawberry.type
class RefundInvoiceModel(RefundInvoiceBase):
    pass
    
@strawberry.type
class RefundInvoiceQueryOutput(RefundInvoiceBase):

    @strawberry.field
    def signed_refund_invoice_path(self) -> Optional[str]:
        # Logic to generate signed URL for refund_invoice_path
        return generate_signed_url(self.refund_invoice_path)

    @strawberry.field
    def signed_problem_item_path(self) -> Optional[str]:
        # Logic to generate signed URL for problem_item_path
        return generate_signed_url(self.problem_item_path)

