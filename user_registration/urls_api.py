from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import UserViewSet, DiscountViewSet, TireStorageViewSet, ServiceAppointmentViewSet

# Настройка маршрутов API с использованием DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'discounts', DiscountViewSet)
router.register(r'tirestorage', TireStorageViewSet)
router.register(r'serviceappointments', ServiceAppointmentViewSet)

# Основные маршруты API
urlpatterns = [
    path('', include(router.urls)),  # Включение маршрутов API
]
