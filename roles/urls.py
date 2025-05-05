from django.urls import path
from .views import RoleView

app_name = "roles"

urlpatterns = [
    path("roles", RoleView.as_view(), name="role-list-create"),
]
