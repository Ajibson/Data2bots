from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [path("payment/user-payment/", views.users_payment, name="user_payment")]
