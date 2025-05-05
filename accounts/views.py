from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from math import ceil
from django.utils.decorators import method_decorator

from roles.models import Role
from .models import Account
from .serializers import AccountSerializer
from auth_custom.decorators import check_role

class AccountView(APIView):
    """
    API để xử lý danh sách tài khoản (GET) và tạo tài khoản mới (POST).
    """

    def get(self, request):
        page = request.query_params.get("page", 1)
        limit = request.query_params.get("limit", 10)
        keyword = request.query_params.get("keyword", None)
        try:
            page = int(page)
            limit = int(limit)
        except ValueError:
            return Response(
                {"error": "Page and limit must be integers."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        accounts = Account.objects.all()
        # Lọc theo keyword nếu có
        if keyword:
            accounts = accounts.filter(username__icontains=keyword)

        # Tính toán phân trang
        total_items = accounts.count()
        total_pages = ceil(total_items / limit)
        start = (page - 1) * limit
        end = start + limit
        paginated_accounts = accounts[start:end]
        serializer = AccountSerializer(paginated_accounts, many=True)
        return Response(
            {
                "total_items": total_items,
                "total_pages": total_pages,
                "current_page": page,
                "page_size": limit,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountDetailView(APIView):
    """
    API để xử lý chi tiết, cập nhật và xóa tài khoản.
    """

    def get(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        serializer = AccountSerializer(account, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        account = get_object_or_404(Account, pk=pk)
        account.delete()
        return Response(
            {"message": "Account deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


@method_decorator(check_role(["ADMIN", "SUPER_USER"]), name="dispatch")
class AssignRoleView(APIView):
    """
    API để gắn role cho người dùng.
    """

    def put(self, request, pk):
        # Lấy người dùng dựa trên pk
        account = get_object_or_404(Account, pk=pk)

        # Lấy danh sách role_codes từ request
        role_codes = request.data.get("role_codes", [])
        if not isinstance(role_codes, list):
            return Response(
                {"error": "role_codes must be a list."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Lấy các role từ database
        roles = Role.objects.filter(code__in=role_codes)
        if not roles.exists():
            return Response(
                {"error": "One or more roles do not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Gắn các role cho người dùng
        # account.roles.add(*roles)
        account.roles.set(roles)

        # Serialize và trả về thông tin người dùng
        serializer = AccountSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
