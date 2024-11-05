from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, personal_cabinet, book_service, login_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('personal_cabinet/', personal_cabinet, name='personal_cabinet'),
    path('book_service/', book_service, name='book_service'),
]


