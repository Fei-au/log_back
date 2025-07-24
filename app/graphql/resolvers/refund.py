import uuid
from datetime import datetime
import pytz
from app.db.mongodb import db_refunds
from typing import List, Optional
from app.graphql.types.refund import RefundInvoiceModel, RefundInvoiceCreateOutput, RefundInvoiceCreateInput, RefundInvoiceQueryOutput, OrderItem, voidRefundInvoiceInput, CompleteRefundInvoiceInput
from dataclasses import asdict
from app.graphql.types.base import BaseInsertOneResponse, BaseUpdateOneResponse
from app.tools.gcp_tools import upload_blob, generate_signed_url

def map_dict_to_refund_invoice(doc: dict) -> RefundInvoiceQueryOutput:
    order_items = doc.pop('order_items')
    return RefundInvoiceQueryOutput(**doc, order_items=[OrderItem(**order_item) for order_item in order_items])

async def refund_invoices(invoice_number: Optional[int], has_completed: Optional[bool], limit: int, offset: int) -> List[RefundInvoiceQueryOutput]:
    refunds_collection = db_refunds["refunds"]
    query = {}
    if has_completed is not None:
        query["has_completed"] = has_completed
    if invoice_number:
        query["invoice_number"] = invoice_number
    
    if invoice_number:
        cursor = refunds_collection.find(query).sort("created_at", -1)
    else:
        cursor = refunds_collection.find(query).skip(offset).limit(limit)
    refund_invoices_list = []
    async for doc in cursor:
        refund_invoices_list.append(map_dict_to_refund_invoice(doc))
    return refund_invoices_list

async def create_refund_invoice_resolver(input: RefundInvoiceCreateInput) -> RefundInvoiceCreateOutput:
    refunds_collection = db_refunds["refunds"]

    # Generate unique ID and refund_id
    new_id = str(uuid.uuid4())
    current_time = datetime.now(pytz.utc)
    # invoice_number + yymmdd + timestamp last four digit
    refund_id = f"{input.invoice_number}{current_time.strftime('%y%m%d')}{str(current_time.timestamp())[-4:]}"
    created_at = current_time.isoformat()

    # Convert OrderItemInput to OrderItem
    order_items_output = []
    for item_input in input.order_items:
        order_items_output.append(
            OrderItem(
                id=item_input.id,
                item_id=item_input.item_id,
                item_number=item_input.item_number,
                lot=item_input.lot,
                pure_price=item_input.pure_price,
                tax=item_input.tax,
                handling_fee=item_input.handling_fee,
                premium_fee=item_input.premium_fee,
                total_price=item_input.total_price,
                refund_amount=item_input.refund_amount,
                after_ordered_status=item_input.after_ordered_status,
                other_status=item_input.other_status,
                pickup_time=item_input.pickup_time,
                sold_time=item_input.sold_time,
                complete=item_input.complete
            )
        )
        
    has_completed=all(item_input.complete for item_input in input.order_items)
    total = sum(item_input.refund_amount for item_input in input.order_items)
    if total != input.total_refund_amount:
        raise ValueError(f"Total refund amount {input.total_refund_amount} does not match the sum of item refunds {total}")
    new_refund_invoice = RefundInvoiceModel(
        _id=new_id,
        refund_id=refund_id,
        order_id=input.order_id,
        invoice_number=input.invoice_number,
        auction=input.auction,
        order_items=order_items_output,
        created_at=created_at,
        has_completed=has_completed,
        completed_time=created_at if has_completed else None,
        total_refund_amount=input.total_refund_amount,
        has_voided=False,
        staff_user_id=input.staff_user_id,
        staff_name=input.staff_name,
    )
    
    from app.tools.generate_pdf import generate_refund_invoice_pdf, generate_problem_item_pdf
    pdf_bytes = generate_refund_invoice_pdf(new_refund_invoice)
    problem_item_pdf = generate_problem_item_pdf(new_refund_invoice)
    refund_invoice_path = upload_blob(pdf_bytes, new_refund_invoice.invoice_number, new_refund_invoice.refund_id, None)
    problem_item_path = upload_blob(problem_item_pdf, new_refund_invoice.invoice_number, new_refund_invoice.refund_id, "problem_item")

    new_refund_invoice.refund_invoice_path = refund_invoice_path
    new_refund_invoice.problem_item_path = problem_item_path
    
    signed_refund_path = generate_signed_url(refund_invoice_path)
    signed_problem_item_path = generate_signed_url(problem_item_path)

    res = await refunds_collection.insert_one(asdict(new_refund_invoice))
    
    return RefundInvoiceCreateOutput(signed_refund_path=signed_refund_path, signed_problem_item_path=signed_problem_item_path, inserted_id=str(res.inserted_id))
    

async def void_refund_invoice_resolver(input: voidRefundInvoiceInput) -> BaseUpdateOneResponse:
    refunds_collection = db_refunds["refunds"]
    res = await refunds_collection.update_one({"refund_id": input.refund_id}, {"$set": {"has_voided": True, "voided_time": datetime.now(pytz.utc).isoformat()}})
    return BaseUpdateOneResponse(modified_count=res.modified_count)

async def complete_refund_invoice_resolver(input: CompleteRefundInvoiceInput) -> BaseUpdateOneResponse:
    refunds_collection = db_refunds["refunds"]
    res = await refunds_collection.update_one({"refund_id": input.refund_id}, {"$set": {"has_completed": True, "completed_time": datetime.now(pytz.utc).isoformat()}})
    return BaseUpdateOneResponse(modified_count=res.modified_count)
