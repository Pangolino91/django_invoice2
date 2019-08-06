from django.urls import path
from django.conf.urls import handler404
from .views import ClientCreate, ClientDetail, ClientList

app_name = 'clients'

urlpatterns = [
    path("add", ClientCreate.as_view(), name="add-client"),
    path("<int:pk>", ClientDetail.as_view(), name="single-client"),
    path("", ClientList.as_view(), name="list-client")
]
