from reportlab.lib.pagesizes import letter, A4
from django.shortcuts import render, get_object_or_404
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from .models import Invoice
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpRequest



class MyPrint:
    def __init__(self, buffer, pagesize):
        # self.id = id
        self.buffer = buffer
        if pagesize == 'A4':
            self.pagesize = A4
        elif pagesize == 'Letter':
            self.pagesize = letter
            self.width, self.height = self.pagesize
    def print_invoice(self, id=None):
        buffer = self.buffer
        doc = SimpleDocTemplate(buffer,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
        pagesize=self.pagesize)
        # Our container for 'Flowable' objects
        elements = []
        # A large collection of style sheets pre-made for us
        styles = getSampleStyleSheet()
        # custom paragraph style
        styles.add(ParagraphStyle(
            name='Enhanced',
            fontSize=15,
            leading=20
        ))
        styles.add(ParagraphStyle(
            name='Enhanced-right',
            fontSize=15,
            leading=12,
            alignment = TA_RIGHT
            # spaceAfter=30
        ))
        styles.add(ParagraphStyle(name='myDetailsHeader', parent=styles['Heading2'], spaceBefore=-70, spaceAfter=0))
        styles.add(ParagraphStyle(name='rightHeader', parent=styles['Heading2']))
        styles.add(ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='below', parent=styles['Normal'],))
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='invoice_header_lastelement', parent=styles['Normal'], spaceAfter=70))
        invoices = Invoice.objects.all()
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        if id:
            invoice = get_object_or_404(Invoice, id=id)
        # APPENDING IMAGE
        if invoice.user.profile.personal_picture:
            company_logo = invoice.user.profile.personal_picture.path
            image = Image(company_logo, width=1*inch, height=1*inch)
            image.hAlign = 'RIGHT'
            image.spaceAfter = -69
            elements.append(image)
        # APPENDING PERSONAL DETAILS
        elements.append(Paragraph(f"{str(invoice.user.profile.companyName)}", styles['myDetailsHeader']))
        elements.append(Paragraph(f"{str(invoice.user.first_name)} {invoice.user.last_name}", styles['Normal']))
        elements.append(Paragraph(f"{str(invoice.user.profile.address)}", styles['Normal']))
        elements.append(Paragraph(f"{str(invoice.user.profile.city)}", styles['Normal']))
        elements.append(Paragraph(f"{str(invoice.user.profile.country)}", styles['Normal']))
        if invoice.user.profile.taxCode:
            elements.append(Paragraph(f"{str(invoice.user.profile.taxCode)}", styles['invoice_header_lastelement']))
        elements.append(Paragraph(f"<font color='blue'> Invoice #{invoice.id}</font>", styles['Heading1']))
        elements.append(Paragraph(f"Invoice Details", styles['Heading2']))
        # for i, invoice in enumerate(invoices):
        tbl_data = [
            [
                Paragraph(f"<b>Client:</b> {str(invoice.client.name)}", styles['Normal']),
                Paragraph(f"<b>Date:</b> {str(invoice.date)}", styles['Normal']),
            ],
        ]
        tbl = Table(tbl_data, colWidths=[3.4*inch, 3.12*inch])
        elements.append(tbl)
        # elements.append(Paragraph(f"<b>Client:</b> {str(invoice.clientName)}", styles['Enhanced']))
        # elements.append(Paragraph(f"<b>Date:</b> {str(invoice.date)}", styles['Enhanced-right']))
        elements.append(Paragraph(str('Elements'), styles['Heading2']))
        # testing
        for element in invoice.elements.all():
            tbl_elements_outer = [
                [
                    Paragraph(f"<b>Element {element.id}:</b> {str(element.name)}", styles['Normal']),
                    Paragraph(f"<b>Price:</b> {str(element.price)} €", styles['Normal'])
                ]
            ]       
            tbl_table = Table(tbl_elements_outer, colWidths=[3.4*inch, 3.12*inch])
            elements.append(tbl_table)
        spacer1 = Spacer(1, 20)
        elements.append(spacer1)
        if invoice.additional_notes:
            elements.append(Paragraph("<b>Additional notes:</b>", styles['Normal'])),
            elements.append(Paragraph(f"{str(invoice.additional_notes)}", styles['Normal']))
        tbl_price_elem = [
            [
                Paragraph("", styles['Normal']),
                Paragraph(f"<b>Total:</b> {str(invoice.total)} €", styles['rightHeader'])
            ]
        ]
        tbl_price = Table(tbl_price_elem, colWidths=[3.4*inch, 3.12*inch])  
        spacer2 = Spacer(1, 20)
        elements.append(spacer2)
        elements.append(tbl_price)
        # elements.append(Paragraph(f"<b>Total:</b> {str(invoice.total)} €", styles['rightHeader']))
        # for element in invoice.element_set.all():
        #     elements.append(Paragraph(str(element.name), styles['Enhanced']))
        doc.build(elements)
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf
