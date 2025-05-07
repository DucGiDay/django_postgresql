from django.db import models
from django.contrib.auth.hashers import make_password
from roles.models import Role 

# Create your models here.
class Account(models.Model):
    id = models.AutoField(primary_key=True)  # ID duy nhất
    created_at = models.DateTimeField(auto_now_add=True)  # Tự động thêm ngày tạo
    updated_at = models.DateTimeField(auto_now=True)  # Tự động cập nhật ngày sửa
    username = models.CharField(max_length=150, unique=True)  # Username duy nhất
    password = models.CharField(max_length=128)  # Mật khẩu đã hash
    full_name = models.CharField(max_length=255, null=True, blank=True)  # Tên đầy đủ
    email = models.EmailField(null=True, blank=True)  # Email
    avatar = models.JSONField(default=dict, blank=True, null=True) 
    roles = models.ManyToManyField(
        Role, related_name="accounts", blank=True
    )  # Liên kết nhiều-nhiều với Role

    def save(self, *args, **kwargs):
        # Hash mật khẩu trước khi lưu
        if not self.pk or "password":
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
