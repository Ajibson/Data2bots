from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import jwt
from datetime import timedelta
from django.conf import settings


class User(AbstractUser):
    # indexing will be done by default since unique is set
    username = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    updated_at = models.DateTimeField(default=timezone.now)

    # we want to user email to login instead of default username
    USERNAME_FIELD = "email"

    # Required fields for admin signup: username in addition to email and password
    REQUIRED_FIELDS = ["username"]

    def __str__(self) -> str:
        return str(self.email)

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):

        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 3 days into the future.

        """
        dt = timezone.now() + timedelta(days=3)

        token = jwt.encode(
            {"id": self.pk, "exp": int(dt.strftime("%s"))},
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return token
