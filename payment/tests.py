from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from account.models import User


class TestPayment(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.payment_url = reverse("payment:user_payment")

        # create general user for all test functions
        self.general_user = User.objects.create(email="t@mail.com")
        self.general_user.set_password("taewo1234")
        self.general_user.save()

    def test_get_user_payment_history_no_auth_token(self):
        response = self.client.get(self.payment_url)

        self.assertEqual(
            "Authentication credentials were not provided.", response.json()["detail"]
        )
        self.assertEqual(response.status_code, 401)

    def test_get_user_payment_history(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.general_user.token)
        response = self.client.get(self.payment_url)

        self.assertIn("payment", response.json().keys())
        self.assertEqual(response.status_code, 200)
