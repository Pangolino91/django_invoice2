from django.shortcuts import render, get_object_or_404, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View

# Create your views here.

def index(request):
    return render(request, 'index.html')
    
class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name='auth/login.html'
    success_message='Successfully logged in'

class UserCreation(View):
    form_class = CustomUserForm
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(self.form_class)
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print('hello')
            form.save()
            new_user = form.cleaned_data['username']
            messages.success(request, f'Welcome {new_user}')
            return HttpResponseRedirect(reverse('invoices:invoice-list'))
            # return HttpResponse('ciao')
        else:
            print(form.cleaned_data)
            cleaned_data2 = super(UserCreation, self)._allowed_methods()
            print(cleaned_data2)
            # return reverse('invoices:invoice-list')
            return render(request, self.template_name, {'form':form})
        ## Here i should have some logic to redirect to different views depending on the `option`


# def user_creation(request):
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return reverse('invoice-list')
#     if request.method == 'GET':
#         form = CustomUserForm()
#     return render(request, 'auth/register.html', {'form': form})