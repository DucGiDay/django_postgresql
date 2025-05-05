from django.urls import path
from .views import AccountDetailView, AccountView

app_name = "accounts"

urlpatterns = [
    path("/accounts", AccountView.as_view(), name="account-list-create"),
    path(
        "accounts/<int:pk>", AccountDetailView.as_view(), name="account-detail"
    ),  # Chi tiết, cập nhật, xóa tài khoản
]
