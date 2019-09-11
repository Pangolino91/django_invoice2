from django.db import models
from django.forms import ModelForm
from .models import ExtendedUser
from django import forms

class ExtendedUserForm(ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ['address', 'city', 'country', 'taxCode', 'personal_picture']
    personal_picture = forms.ImageField(label='Update company logo', required=False, error_messages = {'invalid': "Image files only"}, widget=forms.FileInput)
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['personal_picture'].widget.attrs.update({ 
    #         'id': 'personal_picture_field',
    #         'class': 'personal_picture_field'
    #         })
    #     self.fields['personal_picture'].label = 'Company picture'