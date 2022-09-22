from .models import Payment
from rest_framework import serializers
from product.serializers import OrderSerializer


class PaymentSerializer(serializers.ModelSerializer):

    payment_for = OrderSerializer()

    class Meta:
        model = Payment
        exclude = ["id"]
