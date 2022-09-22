from .models import Product, Order
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ProductSerializer, OrderSerializer, CreateOrderSerializer
from swagger_doc import product_get_doc, order_history_post_doc, create_order_post_doc


@product_get_doc()
@api_view(["GET"])
def get_products(request):
    products = Product.objects.all()

    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)


@order_history_post_doc()
@api_view(["GET"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def order_history(request):
    # orders for the user
    user = request.user

    orders = Order.objects.filter(user=user)

    serializer = OrderSerializer(orders, many=True)

    return Response({"orders": serializer.data})


@create_order_post_doc()
@api_view(["POST"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def create_order(request):

    serializer = CreateOrderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
