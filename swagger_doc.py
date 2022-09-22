from drf_yasg.utils import swagger_auto_schema
from account.serializers import (
    RegistrationSerializer,
    UserSerializer,
    LoginSerializer,
    LoginSerializerOut,
    ProfileUpdate,
)

from payment.serializers import PaymentSerializer
from product.serializers import (
    ProductSerializer,
    CreateOrderSerializer,
    OrderSerializer,
)


def register_post_doc():
    return swagger_auto_schema(
        operation_description="User registration endpoint",
        methods=["POST"],
        request_body=RegistrationSerializer,
        responses={201: UserSerializer, 400: RegistrationSerializer},
        security=[],
    )


def login_post_doc():
    return swagger_auto_schema(
        operation_description="User login endpoint",
        methods=["POST"],
        request_body=LoginSerializer,
        responses={200: LoginSerializerOut, 400: LoginSerializer},
        security=[],
    )


def profile_update_doc():
    return swagger_auto_schema(
        operation_description="User profile update endpoint",
        methods=["PATCH"],
        request_body=ProfileUpdate,
        responses={200: UserSerializer, 400: ProfileUpdate},
        security=[],
    )


def payment_update_doc():
    return swagger_auto_schema(
        operation_description="payment history endpoint",
        methods=["GET"],
        responses={200: PaymentSerializer, 400: None},
        security=[],
    )


def product_get_doc():
    return swagger_auto_schema(
        operation_description="Get all products endpoint",
        methods=["GET"],
        responses={200: ProductSerializer, 400: None},
        security=[],
    )


def create_order_post_doc():
    return swagger_auto_schema(
        operation_description="Order creation endpoint",
        methods=["POST"],
        request_body=CreateOrderSerializer,
        responses={201: CreateOrderSerializer, 400: CreateOrderSerializer},
        security=[],
    )


def order_history_post_doc():
    return swagger_auto_schema(
        operation_description="Order history endpoint",
        methods=["GET"],
        responses={200: OrderSerializer, 400: None},
        security=[],
    )
