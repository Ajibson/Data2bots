from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("products/", views.get_products, name="get_products"),
    path("products/create-order/", views.create_order, name="create_order"),
    path("products/order-history/", views.order_history, name="get_orders"),
]
