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
        "Inv No.",
        "Auction",
        "Count",
        "Created",
        "Staff",
        "Discount",
        "Total"
    ])
    total_invoices = len(d.data)
    total_refund_items = len([item for row in d.data for item in row.order_items])
    total_refund_amount = sum([Decimal(str(row.total_refund_amount)) for row in d.data], Decimal('0.00'))
    for i, row in enumerate(d.data):
        created_at_utc = datetime.fromisoformat(row.created_at) 
        created_at_toronto = created_at_utc.astimezone(timezone('America/Toronto'))
        formatted_created_at = created_at_toronto.strftime('%Y-%m-%d %H:%M:%S')

        writer.writerow([
            str(i + 1) + '-' + ('(Dup) ' + row.invoice_number if row.is_additional else row.invoice_number),
            row.auction,
            len(row.order_items),
            formatted_created_at,
            row.staff_name,
            "",
            row.total_refund_amount,
        ])
        for index, item in enumerate(row.order_items):
            writer.writerow([
                "",
                item.item_number,
                str(index + 1) + ' of ' + str(len(row.order_items)),
                item.after_ordered_status,
                item.other_status,
                item.refund_amount,
            ])
    writer.writerow([
        "Summary",
        "",
        "",
        "",
        "",
        "",
        "",
    ])
    writer.writerow([
        total_invoices,
        "",
        total_refund_items,
        "",
        "",
        "",
        total_refund_amount,
    ])
        
    file_name = generate_refund_export_csv_name()
    destination_file_name = upload_blob(output.getvalue(), "text/csv", file_name)
    return destination_file_name


