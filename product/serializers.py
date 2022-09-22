from rest_framework import serializers
from .models import Order, Product
from account.serializers import UserSerializer


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ["id"]


class OrderSerializer(serializers.ModelSerializer):

    user = UserSerializer()
    product = ProductSerializer()

    class Meta:
        model = Order
        exclude = ["id"]


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        exclude = ["id", "user"]
