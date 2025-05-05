from django.urls import path
from .views import login

app_name = 'auth_custom'

urlpatterns = [
    path('login', login, name='login'),
]