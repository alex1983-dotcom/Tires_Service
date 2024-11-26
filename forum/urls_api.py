from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import CategoryViewSet, ThreadViewSet, PostViewSet

# Настройка маршрутов API с использованием DefaultRouter
router = DefaultRouter()
router.register(r'category_forum', CategoryViewSet)
router.register(r'thread', ThreadViewSet)
router.register(r'post', PostViewSet)

# Основные маршруты API
urlpatterns = [
    path('', include(router.urls)),  # Включение маршрутов API
]
