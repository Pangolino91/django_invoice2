from django.urls import path
from . import views

urlpatterns = [
    path('testsubpage', views.test_sub_page)
]
