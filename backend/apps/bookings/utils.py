"""Utility functions for QR code and PDF ticket generation."""
import io
import qrcode
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A5
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_qr_code(booking):
    """Generate a QR code image for a booking."""
    qr_data = (
        f"HeritageHub Ticket\n"
        f"Booking: {booking.booking_id}\n"
        f"Place: {booking.place.place_name}\n"
        f"Date: {booking.visit_date}\n"
        f"Tickets: {booking.total_tickets}\n"
        f"Status: {booking.status}"
    )
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1a365d", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    filename = f"qr_{booking.booking_id}.png"
    booking.qr_code.save(filename, ContentFile(buffer.read()), save=True)
    return filename


def generate_ticket_pdf(booking):
    """Generate a professional PDF ticket for a booking."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A5,
                            leftMargin=15*mm, rightMargin=15*mm,
                            topMargin=15*mm, bottomMargin=15*mm)

    styles = getSampleStyleSheet()
    elements = []

    # Custom styles
    title_style = ParagraphStyle(
        'Title', parent=styles['Title'],
        fontSize=18, textColor=HexColor('#1a365d'),
        alignment=TA_CENTER, spaceAfter=5*mm
    )
    header_style = ParagraphStyle(
        'Header', parent=styles['Heading2'],
        fontSize=12, textColor=HexColor('#2d6a4f'),
        alignment=TA_CENTER, spaceAfter=3*mm
    )
    normal_style = ParagraphStyle(
        'Normal2', parent=styles['Normal'],
        fontSize=10, spaceAfter=2*mm
    )
    small_style = ParagraphStyle(
        'Small', parent=styles['Normal'],
        fontSize=8, textColor=HexColor('#666666'),
        alignment=TA_CENTER
    )

    # Header
    elements.append(Paragraph("🏛️ HeritageHub", title_style))
    elements.append(Paragraph("E-Ticket / Booking Confirmation", header_style))
    elements.append(Spacer(1, 5*mm))

    # Booking details table
    data = [
        ['Booking ID', str(booking.booking_id)[:8].upper()],
        ['Place', booking.place.place_name],
        ['Location', f"{booking.place.city.city_name}, {booking.place.city.district.state.name}"],
        ['Visit Date', booking.visit_date.strftime('%d %B %Y')],
        ['Time Slot', booking.get_time_slot_display()],
        ['Adults', str(booking.adults)],
        ['Children', str(booking.children)],
        ['Senior Citizens', str(booking.senior_citizens)],
        ['Students', str(booking.students)],
        ['Total Tickets', str(booking.total_tickets)],
        ['Subtotal', f'₹{booking.subtotal}'],
        ['Tax (GST 18%)', f'₹{booking.tax}'],
        ['Discount', f'-₹{booking.discount}'],
        ['Total Amount', f'₹{booking.total_price}'],
        ['Status', booking.status],
        ['Visitor', booking.user.get_full_name() or booking.user.username],
    ]

    table = Table(data, colWidths=[40*mm, 80*mm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#f0f4f8')),
        ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#1a365d')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#e2e8f0')),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (-1, -3), (-1, -3), HexColor('#e6fffa')),
        ('FONTNAME', (-1, -3), (-1, -3), 'Helvetica-Bold'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 5*mm))

    # QR Code
    if booking.qr_code:
        try:
            qr_img = Image(booking.qr_code.path, width=35*mm, height=35*mm)
            elements.append(qr_img)
        except Exception:
            elements.append(Paragraph("QR Code not available", normal_style))

    elements.append(Spacer(1, 3*mm))

    # Footer
    elements.append(Paragraph(
        "This is a computer-generated ticket. Please carry a valid photo ID. "
        "Ticket is non-transferable. For support, contact support@heritagehub.in",
        small_style
    ))

    doc.build(elements)
    buffer.seek(0)
    return buffer
