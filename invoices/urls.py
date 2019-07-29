from django.urls import path
from django.conf.urls import handler404
from . import views
from .views import InvoiceDetailView


urlpatterns = [
    path('list/', views.InvoiceList.as_view(), name='invoice-list'),
    path('<int:pk>/', InvoiceDetailView.as_view(), name='single-invoice'),
    path('add/', views.inline_formset, name="add-elements"),
    path('<int:id>/update', views.update_formset, name="update-element"),
    path('<int:pk>/delete/', views.InvoiceDelete.as_view(), name='delete-invoice'),
    path('<int:id>/pdf', views.test_pdf, name="print-pdf")
]
