from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models



class CustomUserForm(UserCreationForm):
    email = models.EmailField(max_length=200, help_text='Required')
    first_name = models.CharField(max_length=200)

    def save(self, commit=True):
        user = super(CustomUserForm, self).save(commit=False)
        # user.email = self.cleaned_data['email']
        if commit:
            user.save()
            return user

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name')