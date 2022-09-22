from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from account.models import User
from .models import Order, Product


class TestProductOrder(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.products_url = reverse("product:get_products")
        self.order_url = reverse("product:get_orders")
        self.create_order_url = reverse("product:create_order")
        self.product = Product.objects.create(
            name="product1", description="product 1 description"
        )

        # create general user for all test functions
        self.general_user = User.objects.create(email="t@mail.com")
        self.general_user.set_password("taewo1234")
        self.general_user.save()

        self.order = Order.objects.create(
            product=self.product,
            user=self.general_user,
            quantity=10,
            total_price=2000,
            payment_completed=True,
        )

    def test_get_all_products_allow_get_methods_only(self):
        response = self.client.post(self.products_url)
        self.assertEqual(response.status_code, 405)

    def test_get_all_products(self):
        response = self.client.get(self.products_url)

        self.assertEqual(response.status_code, 200)

    def test_create_order_with_no_token(self):
        data = {
            "product": self.product,
            "user": self.general_user,
            "quantity": 250,
            "total_price": 25000,
            "payment_completed": True,
        }
        response = self.client.post(self.create_order_url, data=data)

        self.assertEqual(
            "Authentication credentials were not provided.", response.json()["detail"]
        )
        self.assertEqual(response.status_code, 401)

    def test_create_order_with_token_and_data(self):
        data = {
            "product": self.product.id,
            "quantity": 250,
            "total_price": 25000,
            "payment_completed": True,
        }
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.general_user.token)
        response = self.client.post(self.create_order_url, data=data)

        self.assertEqual(response.json()["product"], self.product.id)
        self.assertEqual(response.status_code, 201)

    def test_get_order_with_no_token(self):
        response = self.client.get(self.order_url)

        self.assertEqual(
            "Authentication credentials were not provided.", response.json()["detail"]
        )
        self.assertEqual(response.status_code, 401)

    def test_get_order_history_per_product_with_correct_token(self):
        # This should returns all the orders made by the user so far
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.general_user.token)
        response = self.client.get(self.order_url)

        self.assertIn("orders", response.json().keys())
        self.assertEqual(response.status_code, 200)
