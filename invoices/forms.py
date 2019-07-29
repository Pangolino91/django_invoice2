from .models import Element, Invoice
from django import forms
from django.forms import inlineformset_factory, formset_factory, modelformset_factory, BaseModelFormSet, modelform_factory, ModelForm, BaseInlineFormSet, Form

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['clientName', 'totalPrice']

# class  BaseInvoiceFormset(BaseModelFormSet):
#     class Meta:
#         pass

InvoiceFormset = modelformset_factory(
    Invoice, 
    fields=('clientName', 'totalPrice'), 
    extra=1
    ) 

# formset = InvoiceFormset(queryset=Invoice.objects.none())

class ElementForm(ModelForm):
    class Meta:
        model = Element
        fields = ['name', 'price']

InlineElementFormset = inlineformset_factory(Invoice, Element, fields=('name', 'price'),
extra=1, can_delete=False)