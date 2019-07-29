"""invoice_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from . import views
from invoices.models import Invoice
from invoices.models import Invoice
from rest_framework import routers, serializers, viewsets
from django.contrib.auth import views as auth_views


# Serializers define the API representation.
class InvoiceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Invoice
        fields = ('client', 'price', 'date')

# ViewSets define the view behavior.
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register('api-invoices', InvoiceViewSet)

urlpatterns = [
    path('', views.index, name="index"),
    # path('login/<int:id>', views.testauth, name="testauth"),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name="login"),
    path('admin/', admin.site.urls),
    path('invoices/', include('invoices.urls')),
    path('auth/', include('auth.urls')),
    path('pages/', include('pages.urls')),
    # path('api/', include(router.urls))
]


handler404 = 'invoices.views.error_404_view'

