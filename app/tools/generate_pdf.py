from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from app.graphql.types.refund import RefundInvoiceModel


# TODO: If the order item expand to the second page, repeat the header again and show page number on each page
def generate_refund_invoice_pdf(data: RefundInvoiceModel):
    buffer = BytesIO()
    page_width, page_height = 3.15 * inch, 2 * inch

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", fontSize=6))
    styles.add(ParagraphStyle(name="RightAlign", fontSize=7, alignment=2))
    styles.add(ParagraphStyle(name="ItemHeader", fontSize=7, fontName="Helvetica-Bold"))
    styles.add(ParagraphStyle(name="ItemText", fontSize=7))

    created_dt = datetime.fromisoformat(data.created_at)
    created_str = created_dt.strftime("%Y-%m-%d %H:%M:%S")
    total_items = len(data.order_items)

    # Header function
    def header(canvas, doc, current_page=1):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 9)
        canvas.drawString(15, page_height - 20, f"Refund Invoice #{data.invoice_number}")
        canvas.setFont("Helvetica", 5)
        canvas.drawString(15, page_height - 28, f"Refund ID: {data.refund_id}")
        canvas.drawString(15, page_height - 35, f"Date: {created_str}")
        canvas.drawString(15, page_height - 42, f"Auction: {data.auction}")
        canvas.drawString(15, page_height - 49, f"Total Items: {total_items}")
        canvas.drawString(15, page_height - 56, f"Page {doc.page}")

        # Company Info (right side)
        y = page_height - 20
        canvas.setFont("Helvetica", 5)
        canvas.drawRightString(page_width - 15, y - 8, "Ruito Trading Inc.")
        canvas.drawRightString(page_width - 15, y - 14, "3495 Laird Road, Unit 10")
        canvas.drawRightString(page_width - 15, y - 20, "Mississauga, ON L5L 5S5")
        canvas.drawRightString(page_width - 15, y - 26, "905-828-8881")
        canvas.restoreState()

    # Custom onPage function to pass page info
    def on_page(canvas, doc):
        current_page = canvas.getPageNumber()
        print(f"Current Page: {current_page}")
        header(canvas, doc, current_page)
        
    # Layout: Create frame that doesn't overlap header
    header_height = 0.7 * inch  # Increased space for header (about 70 pixels)
    bottom_margin = 0.15 * inch
    frame = Frame(
        x1=0.15 * inch,
        y1=0.15 * inch,
        width=page_width - 0.3 * inch,
        height=page_height - header_height - bottom_margin,
        id='normal'
    )
    
    template = PageTemplate(id='RefundTemplate', frames=[frame], onPage=on_page)
    
    # Build table data
    table_data = [[
        Paragraph("<b>Lot#</b>", styles["ItemText"]),
        Paragraph("<b>Description</b>", styles["ItemText"]),
        Paragraph("<b>Refund</b>", styles["ItemText"]),
        Paragraph("<b></b>", styles["ItemText"]),
    ]]

    if not data.order_items:
        raise ValueError("No order items found in the provided data.")

    total_refund = data.total_refund_amount
    for item in data.order_items:
        status = item.other_status if item.after_ordered_status == "Other" else item.after_ordered_status
        complete_str = "✔" if item.complete else "✘"
        refund_amount = item.refund_amount

        table_data.append([
            Paragraph(f"{item.lot} ({item.item_number})", styles["ItemText"]),
            Paragraph(status, styles["ItemText"]),
            Paragraph(f"${refund_amount:.2f}", styles["ItemText"]),
            Paragraph(complete_str, styles["ItemText"]),
        ])

    table = Table(table_data, colWidths=[0.8 * inch, 1.2 * inch, 0.5 * inch, 0.35 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("LINEBELOW", (0, 0), (-1, -1), 0.2, colors.grey),
        ("ALIGN", (2, 1), (2, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))

    elements = [
        Spacer(1, 6),
        table,
        Spacer(1, 6),
        Paragraph(f"Total Refund Amount:  ${total_refund:.2f}", styles["RightAlign"])
    ]

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(page_width, page_height),
        rightMargin=0.15 * inch,
        leftMargin=0.15 * inch,
        topMargin=header_height,
        bottomMargin=bottom_margin,
    )
    
    doc.addPageTemplates([template])
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def generate_problem_item_pdf(data: RefundInvoiceModel):
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

