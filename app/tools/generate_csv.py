from app.graphql.types.output.refund import RefundInvoiceEnhancedOutput
import csv
from io import StringIO
from app.tools.gcp_tools import generate_refund_export_csv_name, upload_blob, generate_signed_url
from decimal import Decimal
from datetime import datetime
from pytz import timezone

def generate_export_csv(d: RefundInvoiceEnhancedOutput) -> bytes:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Refund ID",
        "Invoice Number",
        "Auction",
        "Order Items Count",
        "Created At",
        "Has Completed",
        "Completed Time",
        "Has Voided",
        "Voided Time",
        "Staff Name",
        "Total Refund Amount",
        "Signed Refund Invoice Path"
    ])
    total_invoices = len(d.data)
    total_refund_items = len([item for row in d.data for item in row.order_items])
    total_refund_amount = sum([Decimal(str(row.total_refund_amount)) for row in d.data], Decimal('0.00'))
    for row in d.data:
        created_at_utc = datetime.fromisoformat(row.created_at) 
        created_at_toronto = created_at_utc.astimezone(timezone('America/Toronto'))
        formatted_created_at = created_at_toronto.strftime('%Y-%m-%d %H:%M:%S')

        writer.writerow([
            row.refund_id,
            '(Dup) ' + row.invoice_number if row.is_additional else row.invoice_number,
            row.auction,
            len(row.order_items),
            formatted_created_at,
            "Yes" if row.has_completed else "No",
            row.completed_time,
            "Yes" if row.has_voided else "No",
            row.voided_time,
            row.staff_name,
            row.total_refund_amount,
            row.signed_refund_invoice_path(),
        ])
    writer.writerow([
        "",
        total_invoices,
        "",
        total_refund_items,
        "",
        "",
        "",
        "",
        "",
        "",
        total_refund_amount,
        "",
    ])
        
    file_name = generate_refund_export_csv_name()
    destination_file_name = upload_blob(output.getvalue(), "text/csv", file_name)
    return destination_file_name


