from django.db import models

from accounts.models import Account


# Create your models here.
class RefreshToken(models.Model):
    id = models.AutoField(primary_key=True)  # ID duy nhất
    token = models.CharField(max_length=255, unique=True)  # Token duy nhất
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="refresh_tokens"
    )  # Liên kết với tài khoản
    expiresAt = models.DateTimeField(db_column="expires_at")  # Thời gian hết hạn token

    def __str__(self):
        return f"Token for {self.account.username} (expires at {self.expiresAt})"
