# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, personal_cabinet, book_service

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='user_registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('personal_cabinet/', personal_cabinet, name='personal_cabinet'),
    path('book_service/', book_service, name='book_service'),
]


