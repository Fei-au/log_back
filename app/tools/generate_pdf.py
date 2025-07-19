from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.units import inch, mm


from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from app.graphql.types.refund import RefundInvoice

def generate_refund_invoice_pdf(data: RefundInvoice):
    buffer = BytesIO()
    page_width, page_height = 4 * inch, 6 * inch
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    margin = 0.3 * inch
    line_height = 12
    y = page_height - margin

    # Fonts
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, f"Refund Invoice #{data.invoice_number}")
    y -= line_height

    c.setFont("Helvetica", 8)
    c.drawString(margin, y, f"Refund ID: {data.refund_id}")
    y -= line_height

    dt = datetime.fromisoformat(data.created_at)
    c.drawString(margin, y, f"Created At: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
    y -= line_height

    c.setFont("Helvetica", 10)
    c.drawString(margin, y, f"Auction: {data.auction}")
    y -= line_height * 2

    total_refund = 0.0

    for item in data.order_items:
        if y < margin + line_height * 6:
            c.showPage()
            y = page_height - margin

        # Draw top border for item
        c.setLineWidth(0.3)
        c.line(margin, y, page_width - margin, y)
        y -= line_height

        # Item fields
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin, y, f"Item #{item.item_number}  Lot: {item.lot}")
        y -= line_height

        c.setFont("Helvetica", 9)

        status = (
            item.other_status
            if item.after_ordered_status == "Other"
            else item.after_ordered_status
        )
        c.drawString(margin, y, f"Status: {status}")
        y -= line_height

        refund_str = f"${item.refund_amount:.2f}"
        c.drawString(margin, y, f"Refund: {refund_str}")
        y -= line_height

        complete_str = "✔ Completed" if item.complete else "✘ Not Completed"
        c.drawString(margin, y, f"Status: {complete_str}")
        y -= line_height

        # Bottom border
        c.setLineWidth(0.3)
        c.line(margin, y + 2, page_width - margin, y + 2)
        y -= line_height / 2

        total_refund += item.refund_amount

    # Final total
    if y < margin + line_height * 2:
        c.showPage()
        y = page_height - margin

    y -= line_height
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, f"Total Refund: ${total_refund:.2f}")
    y -= line_height

    c.showPage()
    c.save()

    pdf = buffer.getvalue()
    buffer.close()
    return pdf
