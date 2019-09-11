from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .forms import CustomUserForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.base import View
from .forms import CustomUserUpdateForm
from extendedusers.models import ExtendedUser 
from extendedusers.forms import ExtendedUserForm 
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.conf import settings
# Create your views here.

def index(request):
    return render(request, 'index.html')
    
class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name='auth/login.html'
    success_message='Successfully logged in'

class UserCreation(View):
    form_class = CustomUserForm
    template_name = 'auth/register.html'
    extend_user_form = ExtendedUserForm
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(settings.LOGIN_IF_REGISTERED)
        else:
            form = self.form_class()
            extend_user_form = self.extend_user_form()
            print(self.form_class)
            return render(request, self.template_name, {'form':form, 'ext_user_form':extend_user_form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        extend_user_form = self.extend_user_form(request.POST, request.FILES)
        if form.is_valid() and extend_user_form.is_valid():
            user = form.save()
            additional_info = extend_user_form.save(commit=False)
            additional_info.user = user
            additional_info.save()
            new_user = form.cleaned_data['username']
            messages.success(request, f'Welcome {new_user}')
            return HttpResponseRedirect(reverse('invoices:invoice-list'))
            # return HttpResponse('ciao')
        else:
            # print(form.cleaned_data)
            cleaned_data2 = super(UserCreation, self)._allowed_methods()
            # print(cleaned_data2)
            # return reverse('invoices:invoice-list')
            return render(request, self.template_name, {'form':form, 'ext_user_form':extend_user_form})
        ## Here i should have some logic to redirect to different views depending on the `option`

class UpdateCustomUser(UpdateView):
    model = User
    form_class = CustomUserUpdateForm
    additional_info_form = ExtendedUserForm
    template_name = 'auth/user_update_form.html'
    context_object_name = 'current_user'
    success_url = reverse_lazy('myprofile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["additional_info"] = self.additional_info_form(instance=self.request.user.extendeduser)
        userId = self.request.user.id
        context["user_instance"] = User.objects.get(id=userId)
        return context
    
    # def get_success_url(self, **kwargs):
    #     # super().get_success_url()
    #     return HttpResponseRedirect(reverse_lazy('invoices:invoice-list'))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, instance=self.request.user)
        extend_user_form = self.additional_info_form(request.POST, request.FILES, instance=self.request.user.extendeduser)
        if form.is_valid() and extend_user_form.is_valid():
            user = form.save()
            additional_info = extend_user_form.save(commit=False)
            additional_info.user = user
            additional_info.save()
            messages.success(request, 'Your details have been successfully updated!')
            # new_user = form.cleaned_data['username']
            # messages.success(request, f'Welcome {new_user}')
            return HttpResponseRedirect(reverse('myprofile'))
            # return HttpResponse('ciao')
        else:
            # print(form.cleaned_data)
            cleaned_data2 = super(UpdateCustomUser, self)._allowed_methods()
            # print(cleaned_data2)
            # return reverse('invoices:invoice-list')
            return render(request, self.template_name, {'form':form, 'additional_info':extend_user_form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('myprofile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'auth/change_password.html', {
        'form': form
    })

# def user_creation(request):
#     if request.method == 'POST':
#         form = CustomUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return reverse('invoice-list')
#     if request.method == 'GET':
#         form = CustomUserForm()
#     return render(request, 'auth/register.html', {'form': form})