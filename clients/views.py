from django.shortcuts import render, redirect
from .models import Client
from invoices.models import Invoice
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib import messages
from django.views.generic.list import ListView
# from .urls import *

# Create your views here.

class ClientCreate(CreateView):
    model = Client
    fields = ['name', 'surname', 'address', 'city', 'country', 'taxCode']
    template_name = 'clients/add.html'
    success_url = reverse_lazy("clients:list-client")
    #  begin experiment

    # def testing_related_actions(self):
    #     self.addingshit = 'shit added'
    #     print(self.addingshit)
    
    def post(self, request, *args, **kwargs):
        messages.success(self.request, 'Client created successfully')
        # self.testing_related_actions()
        return super().post(request, *args, **kwargs)


    # end experiment


    # def post(self, request, *args, **kwargs):
    #     super().post(self, request, *args, **kwargs)

    # def get_success_url(self):
    #     # return HttpResponseRedirect("invoices:invoice-list")
    #     return super().get_success_url()

class ClientDetail(DetailView):
    model = Client
    template_name = "clients/single.html"
    context_object_name = 'merda'
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

class ClientList(ListView):
    model = Client
    template_name = 'clients/list.html'
    context_object_name = "mylist"
    paginate_by = 5

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context[""] = 
    #     return context
    
