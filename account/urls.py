from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", views.login, name="login"),
    path("accounts/update_profile/", views.update_profile, name="profile_update"),
]
