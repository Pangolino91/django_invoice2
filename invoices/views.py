from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, FileResponse, HttpResponseRedirect, Http404
from django.template import Context
from .forms import InvoiceForm, InvoiceFormset, InlineElementFormset, ElementForm, InlineElementFormsetUpdate
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
from invoice_project.utils import VerificationRequiredMixin, verification_required

# to create  pdf
import io
from reportlab.pdfgen import canvas

# Invoices List view

class InvoiceList(VerificationRequiredMixin, ListView):
    model = Invoice
    ordering = ['date']
    paginate_by = 10

    def get_queryset(self):
        current_user = self.request.user
        queryset = current_user.invoices.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = {}
        context = super().get_context_data(**context)
        return context

# Single invoice View

class InvoiceDetailView(VerificationRequiredMixin, DetailView):

    model = Invoice

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context
    
# create new invoice and related elements


@verification_required
def inline_formset(request):
    invoice = Invoice()
    user = request.user
    user_clients = user.clients
    invoice_form = InvoiceForm(instance=invoice)
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, userid=user.id)
        formset = InlineElementFormset(request.POST)
        if invoice_form.is_valid():
            created_invoice = invoice_form.save(commit=False)
            formset = InlineElementFormset(request.POST, instance=created_invoice)
            if formset.is_valid():
                print(formset.cleaned_data)
                print(invoice_form.cleaned_data)
                invoice_form.clean()
                created_invoice.user = user
                created_invoice.save()
                formset.save()
                messages.success(request, 'Invoice created successfully.')
                return HttpResponseRedirect(reverse('invoices:invoice-list'))
    else:
        if not user.clients.all():
            messages.info(request, 'You need to create at least one client before creating invoices')
        invoice_form = InvoiceForm(instance=invoice, userid=user.id)
        formset = InlineElementFormset()
    return render(request, 'invoices/testinlineform.html', {
        'invoice_form': invoice_form,
        'formset': formset,
        'user_clients': user_clients
        })

# invoice update view
@verification_required
def update_formset(request, id):
    user = request.user
    invoice = Invoice.objects.get(id=id)
    elements = invoice.elements.all()
    invoice_form = InvoiceForm(instance=invoice)
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST, instance=invoice, userid=user.id)
        formset = InlineElementFormsetUpdate(request.POST, instance=invoice)
        if invoice_form.is_valid():
            print('invoice is valid')
            created_invoice = invoice_form.save()
            formset = InlineElementFormsetUpdate(request.POST, instance=created_invoice)
            # print(formset)
            if formset.is_valid():
                print('Elements are valid')
                print(formset.cleaned_data)
                # print(invoice_form.cleaned_data)
                created_invoice.save()
                formset.save()
                messages.success(request, 'Invoice updated correctly!')
                return HttpResponseRedirect(reverse('invoices:invoice-list'))
            # else:
            #     print(formset.errors)
            #     return HttpResponseRedirect(reverse('invoices:invoice-list'))
    else:
        invoice_form = InvoiceForm(instance=invoice, userid=user.id)
        formset = InlineElementFormsetUpdate(instance=invoice)
    return render(request, 'invoices/testinlineform_update.html', {
        'invoice_form': invoice_form,
        'formset': formset
        })


class InvoiceDelete(VerificationRequiredMixin, DeleteView):
    model = Invoice
    success_url = reverse_lazy('invoices:invoice-list')

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

# class testView(View):
#     testattribute = 'test attribute'

#     def get(self, *args, **kwargs):
        



@verification_required
def test_pdf(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{invoice.date}-{invoice.client.name}.pdf"'

    buffer = io.BytesIO()

    report = MyPrint(buffer, 'Letter')
    pdf = report.print_invoice(id)

    response.write(pdf)
    return response

    