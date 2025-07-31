from reportlab.platypus import SimpleDocTemplate, BaseDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from app.graphql.types.model.refund import RefundInvoiceModel
from reportlab.lib.enums import TA_CENTER


page_width, page_height = 2.85 * inch, 2 * inch
header_height = 0.57 * inch

def draw_image_overlay(canvas: canvas.Canvas, doc):
    data = getattr(doc, '_data', None)
    if not data.has_completed:
        return
    if doc.page == 1:
            width = page_width / 2
            height = width / 1.42
            canvas.drawImage(
                'app/assets/completed2.png',
                x=(page_width - width) / 2,
                y=(page_height - height) - 0.1 * inch,  # position from bottom-left
                width=width,
                height=height,
                mask='auto'
            )
        
def draw_header(canvas: canvas.Canvas, doc):
    data = getattr(doc, '_data', None)
    created_str = getattr(doc, '_created_at', '')
    total_item_count = getattr(doc, '_total_item_count', 0)
    
  
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(12, page_height - 15, f"Refund Invoice #{data.invoice_number}")
    y = page_height - 15
    canvas.setFont("Helvetica", 6)
    canvas.drawString(12, y - 6, f"Refund ID: {data.refund_id}")
    canvas.drawString(12, y - 12, f"Date: {created_str}")

    # Company Info (right side)
    canvas.setFont("Helvetica", 6)
    canvas.drawRightString(page_width - 12, y - 6, f"Auction: {data.auction}")
    canvas.drawRightString(page_width - 12, y - 12, f"Total Items: {total_item_count}")
    canvas.drawRightString(page_width - 12, y - 18, f"Page {doc.page}")
    canvas.restoreState()
        
class RefundInvoicePDFTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        
        frame = Frame(
            x1=0.15 * inch,
            y1=0.15 * inch,
            width=page_width - 0.3 * inch,
            height=page_height - header_height,
            id='normal'
        )
            
        template = PageTemplate(id='RefundTemplate', frames=[frame], onPage=draw_header, onPageEnd=draw_image_overlay)
        self.addPageTemplates([template])
        
def generate_refund_invoice_pdf(data: RefundInvoiceModel):

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Small", fontSize=6, leading=6))
    styles.add(ParagraphStyle(name="ItemHeader", fontSize=6, leading=6, fontName="Helvetica-Bold"))
    item_text_style = ParagraphStyle(name="ItemText", fontSize=8, leading=8, fontName="Helvetica-Bold")
    styles.add(ParagraphStyle(name="RightAlign", parent=item_text_style, alignment=2))
    styles.add(item_text_style)


    # Build table data
    table_data = [
        [
            Paragraph("<b>Lot#</b>", styles["ItemHeader"]),
            Paragraph("<b>Description</b>", styles["ItemHeader"]),
            Paragraph("<b>Refund</b>", styles["ItemHeader"]),
        ]
    ]

    if not data.order_items:
        raise ValueError("No order items found in the provided data.")

    total_refund = data.total_refund_amount
    for item in data.order_items:
        status = item.after_ordered_status + (', ' + item.other_status if item.other_status else '')
        refund_amount = item.refund_amount

        table_data.append([
            Paragraph(f"{item.lot} ({item.item_number})", styles["ItemText"]),
            Paragraph(status, styles["ItemText"]),
            Paragraph(f"${refund_amount}", styles["ItemText"]),
        ])

    table = Table(table_data, colWidths=[0.75 * inch, 1.45 * inch, 0.41 * inch], rowHeights=[3* mm] + [None] * (len(table_data)-1))
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("LINEBELOW", (0, 0), (-1, -1), 1.0, colors.grey),
        ("ALIGN", (2, 1), (2, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),  # Vertically center the header row
        ("VALIGN", (0, 1), (-1, -1), "TOP"),  # Vertically align the content rows to the top
        # ("FONTSIZE", (0, 0), (-1, -1), 1.0),  # Reduced font size from 6 to 2.4
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
    ]))

    elements = [
        table,
        Spacer(1, 3),
        Paragraph(f"Total Refund Amount:  ${total_refund:.2f}", styles["RightAlign"])
    ]


    created_dt = datetime.fromisoformat(data.created_at)
    created_str = created_dt.strftime("%Y-%m-%d %H:%M:%S")
    total_item_count = len(data.order_items)
    buffer = BytesIO()
    
    doc = RefundInvoicePDFTemplate(
        buffer,
        pagesize=(page_width, page_height),
        rightMargin=0.12 * inch,
        leftMargin=0.12 * inch,
        topMargin=header_height,
        bottomMargin=0,
    )
    doc._data = data
    doc._created_at = created_str
    doc._total_item_count = total_item_count

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

