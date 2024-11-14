from django.contrib.auth import views as auth_views
from django.urls import path
from .views import RegisterView, LoginView, PersonalCabinetView, BookServiceView, ServiceAppointmentListView, ServiceAppointmentDetailView, UserListView, UserDetailView, AdminLoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('login/', LoginView.as_view(), name='login'),  # Вход в систему
    path('personal_cabinet/', PersonalCabinetView.as_view(), name='personal_cabinet'),  # Личный кабинет
    path('book_service/', BookServiceView.as_view(), name='book_service'),  # Запись на обслуживание
    path('appointments/', ServiceAppointmentListView.as_view(), name='appointment-list'),  # Список записей на обслуживание
    path('appointments/<int:pk>/', ServiceAppointmentDetailView.as_view(), name='appointment-detail'),  # Детали записи на обслуживание
    path('users/', UserListView.as_view(), name='user-list'),  # Список пользователей
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  # Детали пользователя

    # Маршрут для входа в админку через email
    path('admin/login/', AdminLoginView.as_view(), name='admin_login'),
]







