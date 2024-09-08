from django.urls import path
from .views import register, select_by_user

urlpatterns = [
    path('select-user-type/', select_by_user, name='select_by_user'),
    path('register/', register, name='register'),
]
