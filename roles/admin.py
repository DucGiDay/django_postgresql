from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Role

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'role_name')  # Hiển thị các trường trong admin
    search_fields = ('code', 'role_name')  # Thêm chức năng tìm kiếm