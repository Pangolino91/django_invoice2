from django.shortcuts import render, redirect
from .models import Client
from invoices.models import Invoice
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.views.generic.list import ListView
from invoice_project.utils import verification_required, VerificationRequiredMixin
# from .urls import *

# Create your views here.

class ClientCreate(VerificationRequiredMixin, CreateView):
    model = Client
    fields = ['name', 'surname', 'companyName', 'address', 'city', 'country', 'taxCode']
    template_name = 'clients/add.html'
    success_url = reverse_lazy("clients:list-client")
    #  begin experiment

    # def testing_related_actions(self):
    #     self.addingshit = 'shit added'
    #     print(self.addingshit)
    
    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Client created successfully')
        # self.testing_related_actions()
        # print(self.request.user)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        current_user = self.request.user
        form.instance.user = current_user
        # print(form.clean())
        self.object = form.save()
        return super().form_valid(form)

class ClientDelete(VerificationRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list-client')
    template_name = 'clients/delete.html'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Client deleted successfully')
        # self.testing_related_actions()
        # print(self.request.user)
        return super().post(request, *args, **kwargs)
        
class ClientDetail(VerificationRequiredMixin, UpdateView):
    model = Client
    fields = ['name', 'surname', 'companyName', 'address', 'city', 'country', 'taxCode']
    template_name = "clients/single.html"
    context_object_name = 'client'
    success_url = reverse_lazy("clients:list-client")

    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Client modified successfully')
        # self.testing_related_actions()
        # print(self.request.user)
        return super().post(request, *args, **kwargs)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["addingInvoice"] = Invoice.objects.get(id=1)
    #     return context
    
    # def get(self, request, *args, **kwargs):
    #     self.object = super().get_object()
    #     context = super().get_context_data(**kwargs)
    #     context["addingInvoice"] = Invoice.objects.get(id=1)
    #     return render(request, self.template_name, {
    #         'client': self.object,
    #         'addingInvoice': context
    #         })

    #  USLEESS CALL SINCE I DO NOT DO ANYTHING MORE
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    # def get_context_object_name(self, obj):
    #     single_client = super().get_context_object_name(obj)
    #     return single_client
    
    # def get(self, request, *args, **kwargs):
    #     return render(request, self.template_name, {'ciao': self.get_object()})

class ClientList(VerificationRequiredMixin, ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = "mylist"
    paginate_by = 5


    def get_queryset(self):
        current_user = self.request.user
        queryset = current_user.clients.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
