from django.urls import path
from django.conf.urls import handler404
from .views import ClientCreate, ClientDetail, ClientList, ClientDelete
from django.contrib.auth.decorators import login_required

app_name = 'clients'

urlpatterns = [
    path("add", login_required(ClientCreate.as_view()), name="add-client"),
    path("<int:pk>", login_required(ClientDetail.as_view()), name="single-client"),
    path("<int:pk>/delete", login_required(ClientDelete.as_view()), name="delete-client"),
    path("", login_required(ClientList.as_view()), name="list-client")
]
