from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from payment.models import Payment
from .serializers import PaymentSerializer
from swagger_doc import payment_update_doc


@payment_update_doc()
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def users_payment(request):
    users_payment = Payment.objects.filter(user=request.user)

    payment_serializer = PaymentSerializer(users_payment, many=True)

    return Response({"payment": payment_serializer.data}, status=status.HTTP_200_OK)
