from rest_framework import viewsets
from .models import User, Discount, TireStorage, ServiceAppointment
from .serializers import UserSerializer, DiscountSerializer, TireStorageSerializer, ServiceAppointmentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = DiscountSerializer


class TireStorageViewSet(viewsets.ModelViewSet):
    queryset = TireStorage.objects.all()
    serializer_class = TireStorageSerializer


class ServiceAppointmentViewSet(viewsets.ModelViewSet):
    queryset = ServiceAppointment.objects.all()
    serializer_class = ServiceAppointmentSerializer

