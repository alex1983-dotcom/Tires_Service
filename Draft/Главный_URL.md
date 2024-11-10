`ProffShina\URL`
```
from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static
from user_registration import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('content/', include('content.urls')),  # Маршруты приложения content
    path('user/', include('user_registration.urls')),  # Маршруты приложения user_registration
    path('api/', include('user_registration.urls_api')),  # Маршруты API
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # Медиа-файлы
    path('login/', user_views.login_view, name='login'),  # Логин
    path('logout/', auth_views.LogoutView.as_view(next_page='home_page'), name='logout'),  # Логаут
    path('personal_cabinet/', user_views.personal_cabinet, name='personal_cabinet'),  # Личный кабинет
    path('', include('content.urls')),  # Главная страница
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Медиа-файлы в режиме отладки
```

