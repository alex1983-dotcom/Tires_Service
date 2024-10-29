from django.db import models
from django.urls import path
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
]


