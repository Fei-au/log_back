import strawberry
from app.graphql.resolvers.refund import refund_invoices
from typing import List
from app.graphql.types.refund import RefundInvoiceCreateOutput, RefundInvoiceCreateInput, voidRefundInvoiceInput, CompleteRefundInvoiceInput, RefundInvoiceQueryOutput
from app.graphql.resolvers.refund import create_refund_invoice_resolver, void_refund_invoice_resolver, complete_refund_invoice_resolver
from app.graphql.types.base import BaseInsertOneResponse, BaseUpdateOneResponse
from typing import Optional

@strawberry.type
class Query:
    @strawberry.field
    async def refund_invoices(self, invoice_number: Optional[int]=None, has_completed: Optional[bool]=None, limit: int = 10, offset: int = 0) -> List[RefundInvoiceQueryOutput]:
        return await refund_invoices(invoice_number, has_completed, limit, offset)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_refund_invoice(self, input: RefundInvoiceCreateInput) -> RefundInvoiceCreateOutput:
        return create_refund_invoice_resolver(input)
    
    @strawberry.mutation
    def void_refund_invoice(self, input: voidRefundInvoiceInput) -> BaseUpdateOneResponse:
        return void_refund_invoice_resolver(input)
    
    @strawberry.mutation
    def complete_refund_invoice(self, input: CompleteRefundInvoiceInput) -> BaseInsertOneResponse:
        return complete_refund_invoice_resolver(input)