import random
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
import jwt
from account.models import User
from django.conf import settings
from django.contrib.auth.hashers import check_password


class TestRegisterEndpoints(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.regsiter_url = reverse("account:register")

        # create general user for all test functions
        self.general_user = User.objects.create(
            email="t@mail.com", first_name="a", last_name="b"
        )
        self.general_user.set_password("taewo1234")
        self.general_user.save()

    def test_no_get_method_allowed(self) -> None:
        response = self.client.get(self.regsiter_url)
        self.assertEqual(response.status_code, 405)

    def test_api_register_no_data(self) -> None:
        response = self.client.post(self.regsiter_url)
        for key in ["email", "password"]:
            self.assertIn(key, response.json().keys())
        self.assertTrue(response.status_code, 400)

    def test_api_register_no_valid_data(self) -> None:
        wrong_passwords = ["aze12", "1234747449494", "azeezybdjhddhdhd"]
        wrong_emails = ["a", "@mail.com"]
        for password in wrong_passwords:
            data = {"email": random.choice(wrong_emails), "password": password}
            response = self.client.post(self.regsiter_url, data=data)
            for key in ["email", "password"]:
                self.assertIn(key, response.json().keys())
        self.assertEqual(response.status_code, 400)

    def test_api_register_valid_data(self) -> None:
        data = {"email": "a@mail.com", "password": "azeez1233"}

        response = self.client.post(self.regsiter_url, data=data)
        self.assertIn("success", response.json().keys())
        self.assertEqual(response.status_code, 201)

    def test_full_name_and_str_method_and_short_name_returned(self):
        self.assertEqual("a b", self.general_user.get_full_name())
        self.assertEqual("a", self.general_user.get_short_name())
        self.assertEqual("t@mail.com", self.general_user.__str__())


class TestLogin(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.login_url = reverse("account:login")
        self.user = User.objects.create(email="a@mail.com")
        self.user.set_password("ajsjsj@9494")
        self.user.save()

    def test_no_get_method_allow(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 405)

    def test_login_with_postmethod_no_data(self):
        response = self.client.post(self.login_url)
        for key in ["email", "password"]:
            self.assertIn(key, response.json().keys())
        self.assertTrue(response.status_code, 400)

    def test_login_with_post_method_with_wrong_data(self):
        data = {"email": "t@mail.com", "password": "ahggd8889"}
        response = self.client.post(self.login_url, data=data)

        self.assertIn("Invalid credentials supplied", response.json()["errors"])

    def test_login_with_postmethod_with_valid_data(self):
        data = {"email": "a@mail.com", "password": "ajsjsj@9494"}
        response = self.client.post(self.login_url, data=data)

        # assert user id from the returned token to the token of the user
        token = response.json().get("token")

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

        self.assertEqual(payload["id"], self.user.id)
        self.assertEqual(response.status_code, 200)


class TestUpdateProfile(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.update_profile = reverse("account:profile_update")
        self.user = User.objects.create(email="a@mail.com")
        self.user.set_password("ajsjsj@9494")
        self.user.save()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.user.token)

    def test_no_get_method_allow(self):
        response = self.client.get(self.update_profile)

        self.assertEqual(response.status_code, 405)

    def test_profile_update_wrong_tokens(self):
        data = {}

        self.client.credentials(HTTP_AUTHORIZATION="Token " + "sjsjsskskk")
        response = self.client.patch(self.update_profile, data=data)

        self.assertIn("Invalid token recieved", response.json()["detail"])
        self.assertEqual(response.status_code, 401)

        self.client.credentials(HTTP_AUTHORIZATION="Boken " + "sjsjsskskk")
        response = self.client.patch(self.update_profile, data=data)

        self.assertIn("expecting Token but got Boken", response.json()["detail"])
        self.assertEqual(response.status_code, 401)

    def test_profile_update_right_token_wrong_email_password_format(self):
        wrong_passwords = ["aze12", "1234747449494", "azeezybdjhddhdhd"]
        for password in wrong_passwords:
            data = {"email": "a.mail", "password": password}
            response = self.client.patch(self.update_profile, data=data)
            for key in ["email", "password"]:
                self.assertIn(key, response.json().keys())
                self.assertEqual(response.status_code, 400)

    def test_profile_update_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        data = {"email": "c@mail.com", "password": "password123"}
        response = self.client.patch(self.update_profile, data=data)

        self.assertIn("User account has been banned!!!", response.json()["detail"])
        self.assertEqual(response.status_code, 401)

    def test_profile_update_no_user(self):
        self.user.delete()
        data = {"email": "c@mail.com", "password": "password123"}
        response = self.client.patch(self.update_profile, data=data)

        self.assertIn("Invalid user, please register first.", response.json()["detail"])
        self.assertEqual(response.status_code, 401)

    def test_profile_update_right_token_correct_email_or_password(self):
        data = {"email": "c@mail.com", "password": "password123"}
        response = self.client.patch(self.update_profile, data=data)

        # get the user now
        user = User.objects.filter(email=data["email"])

        # confirm the email changed
        self.assertEqual(user.count(), 1)
        self.assertEqual(user.first().email, data["email"])

        # check if password has changed
        previous_hashed_password = self.user.password
        newly_hashed_password = user.first().password
        self.assertNotEqual(previous_hashed_password, newly_hashed_password)

        # confirm the hashed password
        self.assertTrue(check_password(data["password"], newly_hashed_password))

        self.assertEqual(response.status_code, 200)
