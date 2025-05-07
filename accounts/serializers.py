from rest_framework import serializers

from roles.serializers.response_serializers import RoleResponseSerializer
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    roles = RoleResponseSerializer(
        many=True
    )  # Sử dụng RoleResponseSerializer để trả 1 số thông tin roles

    class Meta:
        model = Account
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True}  # Không trả về mật khẩu trong response
        }


class UpdateAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = fields = ["username", "full_name", "email", "avatar"]
