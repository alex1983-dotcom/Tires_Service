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

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('content/', include('content.urls')),  # Маршруты приложения content
    path('user/', include('user_registration.urls')),  # Маршруты приложения user_registration
    path('api/', include('user_registration.urls_api')),  # Маршруты API
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # Медиа-файлы
    path('login/', auth_views.LoginView.as_view(template_name='user_registration/login.html'), name='login'),  # Логин
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Логаут
    path('', include('content.urls')),  # Главная страница
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Медиа-файлы в режиме отладки
