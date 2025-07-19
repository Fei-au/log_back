import strawberry
from typing import List, Optional

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
class RefundInvoiceInput:
    # order id
    order_id: int
    invoice_number: int
    auction: int
    order_items: List[OrderItemInput]
    staff_user_id: int
    staff_name: str
    
@strawberry.input
class voidRefundInvoiceInput:
    refund_id: str
    has_voided: bool

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

@strawberry.type
class RefundInvoice:
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
    link: Optional[str]
    has_voided: bool
    voided_time: Optional[str]
    staff_user_id: int
    staff_name: str
