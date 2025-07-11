from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from datetime import timedelta
from django.utils.timezone import now
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from accounts.models import Account
from accounts.serializers import AccountSerializer, RegisterSerializer
from auth_custom.models import RefreshToken
from django.conf import settings
from django_postgresql.services.supabase_storage_service import SupabaseStorageService

# ACCESS_TOKEN_LIFETIME = timedelta(minutes=15)  # Thời gian sống của access token
ACCESS_TOKEN_LIFETIME = timedelta(days=1)  # Thời gian sống của access token
REFRESH_TOKEN_LIFETIME = timedelta(days=30)  # Thời gian sống của refresh token


@swagger_auto_schema(
    method="post",
    operation_description="Đăng nhập",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Tên đăng nhập"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Mật khẩu"
            ),
        },
        required=["username", "password"],
    ),
    # responses={200: openapi.Response(description='Đăng nhập thành công')}
)
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
        supabase_service = SupabaseStorageService()
        # url = supabase_service.list_all_files("img-bucket")
        # return Response(
        #     {
        #         "message": "Login successful",
        #         "data": url,
        #     },
        #     status=status.HTTP_200_OK,
        # )
        # url = supabase_service.get_public_url("img-bucket", 'c89670c7-4a7b-4269-8b81-33517303b92b_screenshot.png')
        # return Response(
        #     {
        #         "message": "Login successful",
        #         "data": url,
        #     },
        #     status=status.HTTP_200_OK,
        # )
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method="post",
    operation_description="Đăng ký",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Tên đăng nhập"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Mật khẩu"
            ),
            "full_name": openapi.Schema(
                type=openapi.TYPE_STRING, description="Họ và tên"
            ),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Email"),
            "roles": openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="Roles",
            ),
        },
        required=["username", "password"],
    ),
    # responses={200: openapi.Response(description='Đăng nhập thành công')}
)
@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        if Account.objects.filter(username=username).exists():
            return Response(
                {"error": "User with this username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Account.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
