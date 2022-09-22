from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=40, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate_password(self, value):
        if value.isalpha() or value.isdigit():
            raise serializers.ValidationError(
                "password should be a mixed of letters and numbers"
            )

        return value


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=40, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, creds):
        email = creds.get("email", "")
        password = creds.get("password", "")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials supplied")

        token = user.token

        return {"email": email, "token": token}


class LoginSerializerOut(serializers.Serializer):
    email = serializers.EmailField(required=False)
    token = serializers.CharField(max_length=500)


class ProfileUpdate(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(
        max_length=40, min_length=8, write_only=True, required=False
    )

    def validate_password(self, value):
        if value.isalpha() or value.isdigit():
            raise serializers.ValidationError(
                "password should be a mixed of letters and numbers"
            )

        return value


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ["email"]
