from rest_framework import authentication, exceptions
import jwt
from django.conf import settings

from .models import User


class AuthUser(authentication.BaseAuthentication):
    authentication_header_prefix = "Token"

    def authenticate(self, request):

        request.user = None
        auth_header = authentication.get_authorization_header(request)
        auth_header_prefix = self.authentication_header_prefix.lower()

        auth_header = auth_header.decode("utf-8").split(" ")

        if len(auth_header) <= 1 or len(auth_header) > 2:
            return None

        recieved_prefix = auth_header[0].lower()
        recieved_token = auth_header[1]

        if recieved_prefix != auth_header_prefix:
            raise exceptions.AuthenticationFailed(
                f"expecting Token but got {auth_header[0]}"
            )

        return self.authenticate_user(request, recieved_token)

    def authenticate_user(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        except Exception:
            raise exceptions.AuthenticationFailed("Invalid token recieved")

        user = User.objects.filter(id=payload.get("id")).first()

        if not user:
            raise exceptions.AuthenticationFailed(
                "Invalid user, please register first."
            )

        if not user.is_active:
            raise exceptions.AuthenticationFailed("User account has been banned!!!")

        return (user, token)

    def authenticate_header(self, request):
        return self.authentication_header_prefix
