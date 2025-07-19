from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from app.graphql.types.refund import RefundInvoice


# TODO: If the order item expand to the second page, repeat the header again and show page number on each page
def generate_refund_invoice_pdf(data: RefundInvoice):
    buffer = BytesIO()
    page_width, page_height = 4 * inch, 6 * inch

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", fontSize=8))
    styles.add(ParagraphStyle(name="RightAlign", fontSize=9, alignment=2))
    styles.add(ParagraphStyle(name="ItemHeader", fontSize=9, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="ItemText", fontSize=9))

    created_dt = datetime.fromisoformat(data.created_at)
    created_str = created_dt.strftime("%Y-%m-%d %H:%M:%S")
    total_items = len(data.order_items)

    # Header function
    def header(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 12)
        canvas.drawString(30, page_height - 40, f"Refund Invoice #{data.invoice_number}")
        canvas.setFont("Helvetica", 7)
        canvas.drawString(30, page_height - 52, f"Refund ID: {data.refund_id}")
        canvas.drawString(30, page_height - 62, f"Date: {created_str}")
        canvas.drawString(30, page_height - 72, f"Auction: {data.auction}")
        canvas.drawString(30, page_height - 82, f"Total Items: {total_items}")

        # Company Info (right side)
        y = page_height - 40
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(page_width - 30, y - 12, "Ruito Trading Inc.")
        canvas.drawRightString(page_width - 30, y - 22, "3495 Laird Road, Unit 10")
        canvas.drawRightString(page_width - 30, y - 32, "Mississauga, ON L5L 5S5")
        canvas.drawRightString(page_width - 30, y - 42, "905-828-8881")
        canvas.restoreState()

    # Layout: Create frame that doesn't overlap header
    frame_margin_top = 100  # keep room for header
    frame = Frame(
        x1=0.3 * inch,
        y1=0.4 * inch,
        width=page_width - 0.6 * inch,
        height=page_height - 0.4 * inch - frame_margin_top,
        id='normal'
    )

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(page_width, page_height),
        rightMargin=0.3 * inch,
        leftMargin=0.3 * inch,
        topMargin=frame_margin_top,
        bottomMargin=0.4 * inch
    )

    # Add custom template with header
    template = PageTemplate(id='RefundTemplate', frames=[frame], onPage=header)
    doc.addPageTemplates([template])

    # Build table data
    table_data = [[
        Paragraph("<b>Lot#</b>", styles["ItemText"]),
        Paragraph("<b>Description</b>", styles["ItemText"]),
        Paragraph("<b>Refund</b>", styles["ItemText"]),
        Paragraph("<b></b>", styles["ItemText"]),
    ]]

    total_refund = 0.0
    for item in data.order_items:
        status = item.other_status if item.after_ordered_status == "Other" else item.after_ordered_status
        complete_str = "✔" if item.complete else "✘"
        refund_amount = item.refund_amount
        total_refund += refund_amount

        table_data.append([
            Paragraph(f"{item.lot} ({item.item_number})", styles["ItemText"]),
            Paragraph(status, styles["ItemText"]),
            Paragraph(f"${refund_amount:.2f}", styles["ItemText"]),
            Paragraph(complete_str, styles["ItemText"]),
        ])

    table = Table(table_data, colWidths=[1.0 * inch, 1.6 * inch, 0.6 * inch, 0.5 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.grey),
        ("ALIGN", (2, 1), (2, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
    ]))

    elements = [
        Spacer(1, 12),
        table,
        Spacer(1, 10),
        Paragraph(f"Total Refund Amount:  ${total_refund:.2f}", styles["RightAlign"])
    ]

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generate_problem_item_pdf(data: RefundInvoice):
    # Define your data
    invoice_number = data.invoice_number

    # Create a buffer or a file
    buffer = BytesIO()  # Or use "output.pdf" to write to file directly

    # Set up canvas size: 3.15 x 2.00 inches
    width = 3.15 * inch
    height = 2.00 * inch
    c = canvas.Canvas(buffer, pagesize=(width, height))

    for item in data.order_items:
        text_y = height - 0.3 * inch
        line_spacing = 0.3 * inch

        c.drawString(0.2 * inch, text_y, f"Invoice #: {invoice_number}")
        c.drawString(0.2 * inch, text_y - line_spacing, f"Item #: {item.item_number}")
        c.drawString(0.2 * inch, text_y - 2 * line_spacing, f"Status: {item.after_ordered_status if item.after_ordered_status != 'Other' else item.other_status}")
        
        c.showPage()  # Finish current page and start a new one

    c.save()

    # If using BytesIO, get the value
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data

 