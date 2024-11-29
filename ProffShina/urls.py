"""
URL configuration for ProffShina project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

from user_registration.views import (
    RegisterView,
    LoginView,
    PersonalCabinetView,
    ServiceAppointmentListView,
    ServiceAppointmentDetailView,
    UserListView,
    UserDetailView
)

# Основные маршруты приложения
urlpatterns = [
    path('admin/', admin.site.urls),  # Административная панель
    path('content/', include('content.urls')),  # Маршруты приложения content
    path('user/', include('user_registration.urls')),  # Маршруты приложения регистрации пользователей
    path('api/', include('user_registration.urls_api')),  # Маршруты API для пользователей и записей на обслуживание
    path('forum/', include('forum.urls')),  # Маршруты приложения форума
    path('api/forum/', include('forum.urls_api')),  # Маршруты API для форума
    path('shop/', include('shop.urls')),  # Маршруты приложения shop
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # Обработка медиа-файлов
    path('login/', LoginView.as_view(), name='login'),  # Вход в систему
    path('logout/', auth_views.LogoutView.as_view(next_page='home_page'), name='logout'),  # Выход из системы
    path('personal_cabinet/', PersonalCabinetView.as_view(), name='personal_cabinet'),  # Личный кабинет
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('appointments/', ServiceAppointmentListView.as_view(), name='appointment-list'),  # Список записей на обслуживание
    path('appointments/<int:pk>/', ServiceAppointmentDetailView.as_view(), name='appointment-detail'),  # Детали записи на обслуживание
    path('users/', UserListView.as_view(), name='user-list'),  # Список пользователей
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Детали пользователя
    path('', include('content.urls')),  # Главная страница
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Обработка медиа-файлов в режиме отладки
