from rest_framework import (serializers)
from .models import User, Discount, TireStorage, ServiceAppointment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ['id', 'user', 'total_spent', 'discount_rate']


class TireStorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TireStorage
        fields = ['id', 'user', 'entry_date', 'exit_date', 'daily_rate']


class ServiceAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAppointment
        fields = ['id', 'user', 'car_model', 'service_date', 'service_time', 'additional_info']
