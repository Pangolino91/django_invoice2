from django.urls import path

from .views import verify_account_view

app_name = "extended_users"

urlpatterns = [
    path('verify-account/<uuid:token_uuid>/<str:user_email>/', verify_account_view, name="verify"),
    ]
