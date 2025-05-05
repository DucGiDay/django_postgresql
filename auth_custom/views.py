from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from datetime import timedelta
from django.utils.timezone import now
import jwt

from accounts.models import Account
from accounts.serializers import AccountSerializer
from auth_custom.models import RefreshToken
from django.conf import settings

ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)  # Thời gian sống của access token
REFRESH_TOKEN_LIFETIME = timedelta(days=30)  # Thời gian sống của refresh token

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    SECRET_KEY = settings.SECRET_KEY

    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = Account.objects.get(username=username)
        account_serializer = AccountSerializer(user)
        roles = account_serializer.data.get("roles", [])
        role_codes = [role.get("code") for role in roles]
        if check_password(password, user.password):
            # Tạo access token
            access_token_payload = {
                "user_id": user.id,
                "username": user.username,
                "roles": role_codes,
                "exp": now() + ACCESS_TOKEN_LIFETIME,
            }
            access_token = jwt.encode(
                access_token_payload, SECRET_KEY, algorithm="HS256"
            )

            # Tạo refresh token
            refresh_token_payload = {
                "user_id": user.id,
                "username": user.username,
                "roles": role_codes,
                "exp": now() + REFRESH_TOKEN_LIFETIME,
            }
            refresh_token = jwt.encode(
                refresh_token_payload, SECRET_KEY, algorithm="HS256"
            )

            # Lưu refresh token vào cơ sở dữ liệu
            RefreshToken.objects.create(
                token=refresh_token,
                account=user,
                expiresAt=now() + REFRESH_TOKEN_LIFETIME,
            )

            return Response(
                {
                    "message": "Login successful",
                    "accessToken": access_token,
                    "refreshToken": refresh_token,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
    except Account.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
