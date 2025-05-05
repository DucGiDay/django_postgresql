from rest_framework import serializers
from ..models import Role


class RoleResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = fields = ["code", "roleName"]
