from django.db import models

# Create your models here.

class Role(models.Model):
    code = models.CharField(max_length=100)
    roleName = models.CharField(max_length=200, db_column='role_name')

    def __str__(self):
        return self.code