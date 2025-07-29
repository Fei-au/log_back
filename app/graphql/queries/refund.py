import strawberry
from app.graphql.resolvers.refund import refund_invoice_total_resolver, refund_invoices
from typing import List
from app.graphql.types.output.refund import RefundInvoiceCreateOutput, RefundInvoiceEnhancedOutput, RefundInvoiceTotalOutput
from app.graphql.types.input.refund import QueryInput, RefundInvoiceCreateInput, voidRefundInvoiceInput, CompleteRefundInvoiceInput
from app.graphql.resolvers.refund import create_refund_invoice_resolver, void_refund_invoice_resolver, complete_refund_invoice_resolver
from app.graphql.types.output.base import BaseInsertOneResponse, BaseUpdateOneResponse
from typing import Optional

@strawberry.type
class Query:
    @strawberry.field
    async def refund_invoices(self, input: QueryInput) -> RefundInvoiceEnhancedOutput:
        return await refund_invoices(input)

    @strawberry.field
    async def refund_invoice_total(self) -> RefundInvoiceTotalOutput:
        return await refund_invoice_total_resolver()

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
