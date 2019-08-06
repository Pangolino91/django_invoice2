from .models import Element, Invoice, Client
from django import forms
from django.forms import inlineformset_factory, formset_factory, modelformset_factory, BaseModelFormSet, modelform_factory, ModelForm, BaseInlineFormSet, Form

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['clientName', 'client']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'] = forms.ModelChoiceField(queryset=Client.objects.all())
        
    def clean(self):
        super().clean()
        print(self)
        from django.core.validators import ValidationError

        if self.cleaned_data['client'].name == 'Trollino':
            raise ValidationError({"clientName": "Trollino cannot get an invoice!"})
        

InvoiceFormset = modelformset_factory(
    Invoice, 
    fields=('clientName',), 
    extra=1
    ) 

# formset = InvoiceFormset(queryset=Invoice.objects.none())

class ElementForm(ModelForm):
    class Meta:
        model = Element
        fields = ['name', 'price']

InlineElementFormset = inlineformset_factory(Invoice, Element, fields=('name', 'price'),
extra=1, can_delete=False)