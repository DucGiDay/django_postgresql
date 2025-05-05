from django.db import models

# Create your models here.

class Role(models.Model):
    code = models.CharField(max_length=100)
    role_name = models.CharField(max_length=200)

    def __str__(self):
        return self.code