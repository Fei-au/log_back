from typing import List, Optional
from datetime import datetime
from pytz import timezone, utc
from app.graphql.types.model.refund import RefundInvoiceModel
from app.graphql.types.output.refund import RefundInvoiceEnhancedOutput
import csv


def generate_export_csv(d: RefundInvoiceEnhancedOutput) -> str:
    # Implement CSV generation logic here
    datetime_str = datetime.now(tz='us/eastern').strftime("%Y%m%d_%H%M%S")
    filename = f"exported_refund_invoice_{datetime_str}.csv"
    with open(filename, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for row in d.data:
            writer.writerow([
                row.get("refundId"),
                row.get("invoiceNumber"),
                row.get("auction"),
                row.get("createdAt"),
                row.get("hasCompleted"),
                row.get("completedTime"),
                row.get("hasVoided"),
                row.get("voidedTime"),
                row.get("staffName"),
                row.get("totalRefundAmount"),
                row.get("signedRefundInvoicePath"),
            ])
    return filename