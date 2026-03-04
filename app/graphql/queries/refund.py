import strawberry
from app.graphql.resolvers.refund import mark_as_store_credit_refund_invoice_resolver, refund_invoice_total_resolver, refund_invoices, update_refund_total_resolver
from typing import List
from app.graphql.types.output.refund import ExportCsvOutput, RefundInvoiceCreateOutput, RefundInvoiceEnhancedOutput, RefundInvoiceTotalOutput
from app.graphql.types.input.refund import ExportCsvInput, MarkAsStoreCreditRefundInvoiceInput, QueryInput, RefundInvoiceCreateInput, VoidRefundInvoiceInput, CompleteRefundInvoiceInput, UpdateRefundTotalInput
from app.graphql.resolvers.refund import export_invoices_to_csv_resolver, create_refund_invoice_resolver, void_refund_invoice_resolver, complete_refund_invoice_resolver
from app.graphql.types.output.base import BaseInsertOneResponse, BaseUpdateOneResponse

@strawberry.type
class Query:
    @strawberry.field
    async def refund_invoices(self, input: QueryInput) -> RefundInvoiceEnhancedOutput:
        return await refund_invoices(input)

    @strawberry.field
    async def refund_invoice_total(self) -> RefundInvoiceTotalOutput:
        return await refund_invoice_total_resolver()
    
    @strawberry.field
    async def export_invoices_to_csv(self, input: ExportCsvInput) -> ExportCsvOutput:
        return await export_invoices_to_csv_resolver(input)

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_refund_invoice(self, input: RefundInvoiceCreateInput) -> RefundInvoiceCreateOutput:
        return create_refund_invoice_resolver(input)
    
    @strawberry.mutation
    def void_refund_invoice(self, input: VoidRefundInvoiceInput) -> BaseUpdateOneResponse:
        return void_refund_invoice_resolver(input)
    
    @strawberry.mutation
    def complete_refund_invoice(self, input: CompleteRefundInvoiceInput) -> BaseUpdateOneResponse:
        return complete_refund_invoice_resolver(input)
    
    @strawberry.mutation
    def mark_as_store_credit_refund_invoice(self, input: MarkAsStoreCreditRefundInvoiceInput) -> BaseUpdateOneResponse:
        return mark_as_store_credit_refund_invoice_resolver(input)

    @strawberry.mutation
    def update_refund_total(self, input: UpdateRefundTotalInput) -> BaseUpdateOneResponse:
        return update_refund_total_resolver(input)
