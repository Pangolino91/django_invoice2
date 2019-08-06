from django.urls import path
from django.conf.urls import handler404
from . import views
from .views import InvoiceDetailView
from django.contrib.auth.decorators import login_required

app_name = 'invoices'
urlpatterns = [
    path('list/', login_required(views.InvoiceList.as_view()), name='invoice-list'),
    path('<int:pk>/', login_required(InvoiceDetailView.as_view()), name='single-invoice'),
    path('add/', login_required(views.inline_formset), name="add-elements"),
    path('<int:id>/update', login_required(views.update_formset), name="update-element"),
    path('<int:pk>/delete/', login_required(views.InvoiceDelete.as_view()), name='delete-invoice'),
    path('<int:id>/pdf', login_required(views.test_pdf), name="print-pdf")
]
