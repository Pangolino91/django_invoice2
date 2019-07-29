from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse, FileResponse, HttpResponseRedirect, Http404
from django.template import Context
from .forms import InvoiceForm, InvoiceFormset, InlineElementFormset, ElementForm
from .models import Invoice
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy, reverse
from django.template.loader import get_template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .pdf_models import MyPrint
from django.contrib.auth.models import User
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
# from django_weasyprint import CONTENT_TYPE_PNG, WeasyTemplateResponseMixin
from xhtml2pdf import pisa

# to create  pdf
import io
from reportlab.pdfgen import canvas

# Invoices List view

class InvoiceList(ListView):
    model = Invoice
    ordering = ['date']
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        invoice_list = Invoice.objects.all()
        paginator = Paginator(invoice_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            file_invoice = paginator.page(page)
        except PageNotAnInteger:
            file_invoice = paginator.page(1)
        except EmptyPage:
            file_invoice = paginator.page(paginator.num_pages)

        context['file_invoice'] = file_invoice
        return context

# Single invoice View

class InvoiceDetailView(DetailView):

    model = Invoice

# create new invoice and related elements

def inline_formset(request):
    invoice = Invoice()
    invoice_form = InvoiceForm(instance=invoice)
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        formset = InlineElementFormset(request.POST)
        if invoice_form.is_valid():
            created_invoice = invoice_form.save(commit=False)
            formset = InlineElementFormset(request.POST, instance=created_invoice)
            if formset.is_valid():
                print(formset.cleaned_data)
                print(invoice_form.cleaned_data)
                created_invoice.save()
                formset.save()
                return HttpResponseRedirect(reverse('invoice-list'))
    else:
        invoice_form = InvoiceForm(instance=invoice)
        formset = InlineElementFormset()
    return render(request, 'invoices/testinlineform.html', {
        'invoice_form': invoice_form,
        'formset': formset
        })

# invoice update view

def update_formset(request, id):
    invoice = Invoice.objects.get(id=id)
    elements = invoice.element_set.all
    invoice_form = InvoiceForm(instance=invoice)
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, instance=invoice)
        formset = InlineElementFormset(request.POST, instance=invoice)
        if invoice_form.is_valid():
            created_invoice = invoice_form.save(commit=False)
            formset = InlineElementFormset(request.POST, instance=created_invoice)
            if formset.is_valid():
                print(formset.cleaned_data)
                print(invoice_form.cleaned_data)
                created_invoice.save()
                formset.save()
                return HttpResponseRedirect(reverse('invoice-list'))
    else:
        invoice_form = InvoiceForm(instance=invoice)
        formset = InlineElementFormset(instance=invoice)
    return render(request, 'invoices/testinlineform_update.html', {
        'invoice_form': invoice_form,
        'formset': formset
        })


class InvoiceDelete(DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoice-list')

def error_404_view(request, exception):
    return render(request,'invoices/404.html')

#  this is experimental way to add invoices through formsets (more than 1
# ) but in this case is only one due to options in the forms.py file

# def invoice_form(request):
#     # form = InvoiceFormset()
#     if request.method == 'POST':
#         form = InvoiceFormset(request.POST, queryset=Invoice.objects.none())
#         if form.is_valid():
#             print(form.cleaned_data)
#             form.save()
#             return HttpResponseRedirect(reverse('invoice-list'))
#     else:
#         form = InvoiceFormset(queryset=Invoice.objects.none())
#     return render(request, 'invoices/testforminvoice.html', {'form': form})

# this is simple add invoice method but it only adds invoice
# without possibility to add related elements...quite useless

# def element_form(request):
#     if request.method == 'POST':
#         form = ElementForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('invoice-list'))
#     else:
#         form = ElementForm()
#     return render(request, 'invoices/addelement.html', {'form': form})

# start pdf drawing

@staff_member_required
def test_pdf(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoice.date}-{invoice.clientName}.pdf"'

    buffer = io.BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.print_invoice(id)

    response.write(pdf)
    return response

    