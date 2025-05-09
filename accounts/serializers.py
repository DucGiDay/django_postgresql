from rest_framework import serializers

from roles.models import Role
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

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = fields = ["username", "full_name", "email", "password"]
    def create(self, validated_data):
        # Lấy danh sách role_codes từ validated_data
        role_codes = validated_data.pop("roles", [])
        account = super().create(validated_data)

        # Gắn các roles cho account
        if role_codes:
            roles = Role.objects.filter(code__in=role_codes)
            account.roles.set(roles)

        return account
