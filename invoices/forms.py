from .models import Element, Invoice, Client
from django import forms
from django.forms import inlineformset_factory, formset_factory, modelformset_factory, BaseModelFormSet, modelform_factory, ModelForm, BaseInlineFormSet, Form

class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = ['client']

    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('userid', None)
        super().__init__(*args, **kwargs)
        self.fields['client'] = forms.ModelChoiceField(queryset=Client.objects.filter(user_id=userid))
        
    def clean(self):
        super().clean()
        # print(self)
        from django.core.validators import ValidationError

        

InvoiceFormset = modelformset_factory(
    Invoice, 
    fields=('client',), 
    extra=1
    ) 

# formset = InvoiceFormset(queryset=Invoice.objects.none())

class ElementForm(ModelForm):
    class Meta:
        model = Element
        fields = ['name', 'price']

InlineElementFormset = inlineformset_factory(Invoice, Element, fields=('name', 'price'),
extra=1, can_delete=False)

InlineElementFormsetUpdate = inlineformset_factory(Invoice, Element, fields=('name', 'price'),
extra=0, can_delete=True)