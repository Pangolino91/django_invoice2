from reportlab.lib.pagesizes import letter, A4
from django.shortcuts import render, get_object_or_404
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from .models import Invoice
from django.contrib.auth.models import User


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
        styles.add(ParagraphStyle(name='right', parent=styles['Normal'], alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))
        invoices = Invoice.objects.all()
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        if id:
            invoice = get_object_or_404(Invoice, id=id)
        # else:
        #     invoices = Invoice.objects.all()
        elements.append(Paragraph(f"<font color='blue'> Invoice #{invoice.id}</font>", styles['Heading1']))
        elements.append(Paragraph(f"Invoice Details", styles['Heading2']))
        # for i, invoice in enumerate(invoices):
        tbl_data = [
            [
                Paragraph(f"<b>Client:</b> {str(invoice.client.name)}", styles['Normal']),
                Paragraph(f"<b>Date:</b> {str(invoice.date)}", styles['Normal'])
            ],
        ]
        tbl = Table(tbl_data, colWidths=[3.4*inch, 3.12*inch])
        elements.append(tbl)
        # elements.append(Paragraph(f"<b>Client:</b> {str(invoice.clientName)}", styles['Enhanced']))
        # elements.append(Paragraph(f"<b>Date:</b> {str(invoice.date)}", styles['Enhanced-right']))
        elements.append(Paragraph(str('elements'), styles['Heading2']))
        # testing
        for element in invoice.elements.all():
            tbl_elements_outer = [
                [
                    Paragraph(f"<b>Element Name:</b> {str(element.name)}", styles['Normal']),
                    Paragraph(f"<b>Price:</b> {str(element.price)}", styles['Normal'])
                ]
            ]       
            tbl_table = Table(tbl_elements_outer, colWidths=[3.4*inch, 3.12*inch])
            elements.append(tbl_table)
        elements.append(Paragraph(f"<b>Total Price:</b> {str(invoice.total)}€", styles['Heading2']))
        # for element in invoice.element_set.all():
        #     elements.append(Paragraph(str(element.name), styles['Enhanced']))
        doc.build(elements)
        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        return pdf



# class MyPrint:
#     def __init__(self, buffer, pagesize):
#         # self.id = id
#         self.buffer = buffer
#         if pagesize == 'A4':
#             self.pagesize = A4
#         elif pagesize == 'Letter':
#             self.pagesize = letter
#             self.width, self.height = self.pagesize
#     def print_users(self, id=None):
#         buffer = self.buffer
#         doc = SimpleDocTemplate(buffer,
#         rightMargin=72,
#         leftMargin=72,
#         topMargin=72,
#         bottomMargin=72,
#         pagesize=self.pagesize)
#         # Our container for 'Flowable' objects
#         elements = []

#         # A large collection of style sheets pre-made for us
#         styles = getSampleStyleSheet()
#         styles.add(ParagraphStyle(name='centered', alignment=TA_CENTER))

#         # Draw things on the PDF. Here's where the PDF generation happens.
#         # See the ReportLab documentation for the full list of functionality.
#         users = User.objects.all()
#         if id:
#             user = get_object_or_404(User, id=id)
#         else:
#             user = User.objects.all()
#         elements.append(Paragraph('My User Names', styles['Heading1']))
#         for i, user in enumerate(users):
#             elements.append(Paragraph(str(user.id), styles['Normal']))

#         doc.build(elements)

#         # Get the value of the BytesIO buffer and write it to the response.
#         pdf = buffer.getvalue()
#         buffer.close()
#         return pdf

