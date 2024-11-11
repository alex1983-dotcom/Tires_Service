from django.urls import path
from .views import RegisterView, LoginView, PersonalCabinetView, BookServiceView, ServiceAppointmentListView, ServiceAppointmentDetailView, UserListView, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('personal_cabinet/', PersonalCabinetView.as_view(), name='personal_cabinet'),
    path('book_service/', BookServiceView.as_view(), name='book_service'),
    path('appointments/', ServiceAppointmentListView.as_view(), name='appointment-list'),
    path('appointments/<int:pk>/', ServiceAppointmentDetailView.as_view(), name='appointment-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]




