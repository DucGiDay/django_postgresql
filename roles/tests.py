from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from .models import Role


class RoleModelTest(TestCase):
    def setUp(self):
        self.role = Role.objects.create(code="admin", roleName="Administrator")

    def test_role_str(self):
        self.assertEqual(str(self.role), "admin")  # Kiểm tra __str__

    def test_role_fields(self):
        self.assertEqual(self.role.code, "admin")
        self.assertEqual(self.role.roleName, "Administrator")