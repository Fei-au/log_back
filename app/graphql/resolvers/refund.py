import uuid
from datetime import datetime
import pytz
from app.db.mongodb import db_refunds
from typing import List, Optional
from app.graphql.types.model.refund import RefundInvoiceModel, OrderItem
from app.graphql.types.output.refund import ExportCsvOutput, RefundInvoiceCreateOutput, RefundInvoiceQueryOutput, RefundInvoiceTotalOutput, RefundInvoiceEnhancedOutput
from app.graphql.types.input.refund import ExportCsvInput, MarkAsStoreCreditRefundInvoiceInput, QueryInput, RefundInvoiceCreateInput, VoidRefundInvoiceInput, CompleteRefundInvoiceInput, UpdateRefundTotalInput
from dataclasses import asdict
from app.graphql.types.output.base import BaseUpdateOneResponse
from app.tools.gcp_tools import generate_refund_file_name, upload_blob, generate_signed_url
from decimal import Decimal
from app.tools.generate_csv import generate_export_csv
from app.tools.generate_pdf import generate_refund_invoice_pdf, generate_problem_item_pdf
from app.core.config import celery_app


def map_dict_to_refund_invoice(doc: dict) -> RefundInvoiceQueryOutput:
    order_items = doc.pop('order_items')
    return RefundInvoiceQueryOutput(**doc, order_items=[OrderItem(**order_item) for order_item in order_items])

async def refund_invoices(input: QueryInput) -> RefundInvoiceEnhancedOutput:
    refunds_collection = db_refunds["refunds"]
    invoice_number = input.invoice_number
    has_completed = input.has_completed
    has_voided = input.has_voided
    is_store_credit = input.is_store_credit
    limit = input.limit
    offset = input.offset
    query = {}
    if has_completed is not None:
        query["has_completed"] = has_completed
    if has_voided is not None:
        query["has_voided"] = has_voided
    if invoice_number:
        query["invoice_number"] = invoice_number
    if is_store_credit:
        query["is_store_credit"] = is_store_credit
    if limit is not None and offset is not None:
        cursor = refunds_collection.find(query).skip(offset).limit(limit).sort("created_at", -1)
    else:
        cursor = refunds_collection.find(query).sort("created_at", -1)
    total = await refunds_collection.count_documents(query)
    refund_invoices_list = []
    async for doc in cursor:
        doc["is_store_credit"] = doc.get("is_store_credit", None)
        doc["refund_email"] = doc.get("refund_email", None)
        doc["payment_method"] = doc.get("payment_method", None)
        refund_invoices_list.append(map_dict_to_refund_invoice(doc))
    return RefundInvoiceEnhancedOutput(data=refund_invoices_list, total=total)

async def refund_invoice_total_resolver() -> RefundInvoiceTotalOutput:
    refunds_collection = db_refunds["refunds"]
    total_count = await refunds_collection.count_documents({})
    return RefundInvoiceTotalOutput(total=total_count)

async def export_invoices_to_csv_resolver(input: ExportCsvInput) -> ExportCsvOutput:
    refunds_collection = db_refunds["refunds"]
    ids = input.ids
    if not ids:
        raise ValueError("No IDs provided for export.")

    cursor = refunds_collection.find({"refund_id": {"$in": ids}})
    refund_invoices_list = []
    async for doc in cursor:
        refund_invoices_list.append(map_dict_to_refund_invoice(doc))
    temp_ins = RefundInvoiceEnhancedOutput(data=refund_invoices_list, total=len(refund_invoices_list))
    csv_path = generate_export_csv(temp_ins)
    refunds_collection_exported = db_refunds["refunds_exported"]
    current_time = datetime.now(pytz.utc)
    export_record = {
        "exported_at": current_time.isoformat(),
        "signed_csv_path": csv_path,
        "ids": ids
    }
    await refunds_collection_exported.insert_one(export_record)
    link = generate_signed_url(csv_path)
    return ExportCsvOutput(signed_csv_path=link)

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
                # complete=item_input.complete
            )
        )
        
    # has_completed=all(item_input.complete for item_input in input.order_items)
    total = [Decimal(str(item_input.refund_amount)) for item_input in input.order_items]
    total = sum(total, Decimal('0.00'))
    if total != Decimal(str(input.total_refund_amount)):
        raise ValueError(f"Total refund amount {input.total_refund_amount} does not match the sum of item refunds {total}")
    is_additional = await refunds_collection.count_documents({"invoice_number": input.invoice_number}) > 0
    new_refund_invoice = RefundInvoiceModel(
        _id=new_id,
        refund_id=refund_id,
        order_id=input.order_id,
        invoice_number=input.invoice_number,
        auction=input.auction,
        order_items=order_items_output,
        created_at=created_at,
        has_completed=input.has_completed,
        completed_time=created_at if input.has_completed else None,
        total_refund_amount=input.total_refund_amount,
        has_voided=False,
        staff_user_id=input.staff_user_id,
        staff_name=input.staff_name,
        is_additional=is_additional,
        is_store_credit=input.is_store_credit,
        refund_email=input.refund_email,
        payment_method=input.payment_method,
        invoice_payment_status=input.invoice_payment_status
    )
    
    pdf_bytes = generate_refund_invoice_pdf(new_refund_invoice)
    # Save pdf_bytes locally
    # inv_local_path = save_bytes_to_file(pdf_bytes, new_refund_invoice.invoice_number)
    # inv_public_url = get_public_url(inv_local_path)
    # pi_local_path = save_bytes_to_file(problem_item_pdf, new_refund_invoice.invoice_number + '_problem_item')
    # pi_public_url = get_public_url(pi_local_path)
    problem_item_pdf = generate_problem_item_pdf(new_refund_invoice)
    refund_invoice_name = generate_refund_file_name(new_refund_invoice.invoice_number, new_refund_invoice.refund_id, None)
    problem_item_name = generate_refund_file_name(new_refund_invoice.invoice_number, new_refund_invoice.refund_id, "problem_item")
    refund_invoice_path = upload_blob(pdf_bytes, content_type='application/pdf', destination_blob_name=refund_invoice_name)
    problem_item_path = upload_blob(problem_item_pdf, content_type='application/pdf', destination_blob_name=problem_item_name)

    new_refund_invoice.refund_invoice_path = refund_invoice_path
    new_refund_invoice.problem_item_path = problem_item_path
    
    signed_refund_path = generate_signed_url(refund_invoice_path)
    signed_problem_item_path = generate_signed_url(problem_item_path)

    res = await refunds_collection.insert_one(asdict(new_refund_invoice))
    celery_app.send_task(
        'inventory.tasks.update_items', 
        [
            {
                'id': item.item_id, 
                'status_note': f'{item.after_ordered_status} {item.other_status}' if item.other_status else item.after_ordered_status
            } 
            for item in input.order_items 
            if item.after_ordered_status != 'Missing'
        ]
    )
    return RefundInvoiceCreateOutput(
        signed_refund_path=signed_refund_path,
        signed_problem_item_path=signed_problem_item_path,
        # temp_problem_item_path=pi_public_url,
        # temp_refund_path=inv_public_url,
        inserted_id=str(res.inserted_id)
    )
    
    '''
**Google Cloud Observability**
monitoring logging, error reporting, and fault tracing
    there are free usage allotments
    
**Cloud Monitoring**
Charts
Dashboards
Alerts
    Such as the server down at night
    We recommend alerting on symptoms, and not necessarily causes
    - The type of uptime check can be set to HTTP, HTTPS, or TCP.
    - The resource to be checked can be an App Engine application, a Compute Engine instance, a URL of a host, or an AWS instance or load balancer.
    
Metrics
A metrics scope is the root entity that holds monitoring and configuration information in Cloud Monitoring.
- Every metrics scope is hosted by a specific Google Cloud project, known as the Scoping Project.
- The metrics scope can include the scoping project itself plus up to 375 additional Google Cloud projects. These are called Monitored Projects.
    - By adding projects to a metrics scope, you can view metrics from different environments (like Production, Staging, and Dev) on a single chart without switching project contexts

a role assigned to one person on one project applies equally to all projects monitored by that metrics scope.

In order to give people different roles per project and to control visibility to data, consider placing the monitoring of those projects in separate metrics scopes.


    '''
async def void_refund_invoice_resolver(input: VoidRefundInvoiceInput) -> BaseUpdateOneResponse:
    
    refunds_collection = db_refunds["refunds"]
    # Check if already voided
    existing_refund = await refunds_collection.find_one({"refund_id": input.refund_id, "has_voided": True})
    if existing_refund:
        raise ValueError("This refund invoice has already been voided.")
    res = await refunds_collection.update_one({"refund_id": input.refund_id}, {"$set": {"has_voided": True, "voided_time": datetime.now(pytz.utc).isoformat()}})
    return BaseUpdateOneResponse(modified_count=res.modified_count)

async def complete_refund_invoice_resolver(input: CompleteRefundInvoiceInput) -> BaseUpdateOneResponse:
    refunds_collection = db_refunds["refunds"]
    # Check if already completed
    existing_refund = await refunds_collection.find_one({"refund_id": input.refund_id, "has_completed": True})
    if existing_refund:
        raise ValueError("This refund invoice has already been completed.")
    res = await refunds_collection.update_one({"refund_id": input.refund_id}, {"$set": {"has_completed": True, "completed_time": datetime.now(pytz.utc).isoformat()}})
    return BaseUpdateOneResponse(modified_count=res.modified_count)

async def mark_as_store_credit_refund_invoice_resolver(input: MarkAsStoreCreditRefundInvoiceInput) -> BaseUpdateOneResponse:
    refunds_collection = db_refunds["refunds"]
    # Check if already marked as store credit
    existing_refund = await refunds_collection.find_one({"refund_id": input.refund_id, "is_store_credit": True})
    if existing_refund:
        raise ValueError("This refund invoice has already been marked as store credit.")
    res = await refunds_collection.update_one({"refund_id": input.refund_id}, {"$set": {"is_store_credit": True}})
    return BaseUpdateOneResponse(modified_count=res.modified_count)


async def update_refund_total_resolver(input: UpdateRefundTotalInput) -> BaseUpdateOneResponse:
    refunds_collection = db_refunds["refunds"]
    existing_refund = await refunds_collection.find_one({"refund_id": input.refund_id})
    if not existing_refund:
        raise ValueError("Refund invoice not found.")
    res = await refunds_collection.update_one({"refund_id": input.refund_id}, {"$set": {"total_refund_amount": input.total_refund_amount}})
    return BaseUpdateOneResponse(modified_count=res.modified_count)