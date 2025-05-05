from django.urls import path
from .views import role_list

app_name = 'roles'

urlpatterns = [
    path('/roles', role_list, name='role-list'),
]