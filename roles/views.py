from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import Role
from .serializers.roles_serializers import RoleSerializer


class RoleView(APIView):
    """
    API để xử lý danh sách role (GET) và tạo role mới (POST).
    """

    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Tạo role mới",
        request_body=RoleSerializer,
        responses={201: RoleSerializer, 400: "Dữ liệu không hợp lệ"},
    )
    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(["GET"])
# def role_list(request):
#     roles = Role.objects.all()
#     serializer = RoleSerializer(roles, many=True)
#     return Response(serializer.data)
