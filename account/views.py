from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework import status
from . import serializers
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from swagger_doc import register_post_doc, login_post_doc, profile_update_doc


@transaction.atomic
@register_post_doc()
@api_view(["POST"])
def register(request):
    if request.method == "POST":
        serializer = serializers.RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # the save method is called to have access to the user instance that just got saved
            user = serializer.save()
            user.set_password(serializer.validated_data.get("password"))
            user.save()

            return Response(
                {"success": serializer.data}, status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@login_post_doc()
@api_view(["POST"])
def login(request):
    if request.method == "POST":
        serializer = serializers.LoginSerializer(data=request.data)

        if serializer.is_valid():
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@profile_update_doc()
@api_view(["PATCH"])
@permission_classes(
    [
        IsAuthenticated,
    ]
)
def update_profile(request):
    data = request.data

    serializer = serializers.ProfileUpdate(data=data)

    if serializer.is_valid():
        user = request.user

        if data.get("email"):
            user.email = data.get("email")
            user.save()
        if data.get("password"):
            user.set_password(data.get("password"))
            user.save()

        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
