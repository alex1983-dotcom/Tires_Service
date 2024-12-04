from django.contrib import admin
from user_registration.models import User, Discount, TireStorage, ServiceAppointment
from django.utils.crypto import get_random_string
from dotenv import load_dotenv
import os
import requests
import hashlib

# Загружаем переменные окружения из файла .env
load_dotenv()


class UserAdmin(admin.ModelAdmin):
    """
    Класс для управления моделью пользователя в административной панели.
    """
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)
    exclude = ('password',)  # Исключаем поле password из админки

    def save_model(self, request, obj, form, change):
        """
        Переопределяем метод save_model, чтобы сгенерировать пароль и отправить SMS при создании пользователя.
        """
        try:
            if not change:  # Только при создании нового пользователя
                raw_password = get_random_string(length=8)
                obj.set_password(raw_password)
                obj.save()  # Сначала сохраняем объект пользователя
                self.send_sms(obj.phone_number, f"Ваш новый пароль: {raw_password}")  # Затем отправляем SMS
            else:
                super().save_model(request, obj, form, change)
        except Exception as e:
            print(f"Ошибка при сохранении модели пользователя: {e}")

    def send_sms(self, phone_number, message):
        """
        Функция для отправки SMS-сообщений с использованием RocketSMS API.
        """
        rocketsms_login = os.getenv('ROCKSMS_LOGIN')
        rocketsms_password = os.getenv('ROCKSMS_PASSWORD')
        rocketsms_passhash = hashlib.md5(rocketsms_password.encode('utf-8')).hexdigest()
        rocketsms_url = 'http://api.rocketsms.by/simple/send'

        data = {
            'username': rocketsms_login,
            'password': rocketsms_passhash,
            'phone': phone_number,
            'text': message,
            'priority': 'true'
        }

        try:
            request = requests.post(rocketsms_url, data=data)
            result = request.json()
            status = result['status']
        except Exception as e:
            print('Cannot send SMS: bad or no response from RocketSMS.')
            print(e)
        else:
            if status in ('SENT', 'QUEUED'):
                print('SMS accepted, status: {}'.format(status))
            else:
                print('SMS rejected, status: {}'.format(status))


admin.site.register(User, UserAdmin)


class DiscountAdmin(admin.ModelAdmin):
    """
    Настройка отображения скидок в административной панели.
    """
    list_display = ('user_full_name', 'user_email', 'user_phone_number', 'total_spent', 'calculate_discount')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'user__phone_number')
    list_filter = ('user', 'total_spent')
    raw_id_fields = ('user',)  # Поле автозаполнения для пользователя

    def user_full_name(self, obj):
        """
        Возвращает полное имя пользователя.
        """
        return f"{obj.user.first_name} {obj.user.last_name}"

    def user_email(self, obj):
        """
        Возвращает email пользователя.
        """
        return obj.user.email

    def user_phone_number(self, obj):
        """
        Возвращает номер телефона пользователя.
        """
        return obj.user.phone_number

    user_full_name.short_description = 'Полное имя'
    user_email.short_description = 'Email'
    user_phone_number.short_description = 'Номер телефона'


admin.site.register(Discount, DiscountAdmin)


class TireStorageAdmin(admin.ModelAdmin):
    """
    Настройка отображения информации о хранении шин в административной панели.
    """
    list_display = ('user_full_name', 'user_phone_number', 'entry_date', 'exit_date', 'tire_model', 'tire_size', 'quantity', 'calculate_storage_cost')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'user__phone_number', 'tire_model', 'tire_size', 'quantity')
    list_filter = ('user', 'entry_date', 'exit_date', 'tire_model', 'tire_size')
    autocomplete_fields = ['user']  # Поле автозаполнения для пользователя

    def user_full_name(self, obj):
        """
        Возвращает полное имя пользователя.
        """
        return f"{obj.user.first_name} {obj.user.last_name}"

    def user_phone_number(self, obj):
        """
        Возвращает номер телефона пользователя.
        """
        return obj.user.phone_number

    user_full_name.short_description = 'Полное имя'
    user_phone_number.short_description = 'Номер телефона'


admin.site.register(TireStorage, TireStorageAdmin)


class ServiceAppointmentAdmin(admin.ModelAdmin):
    """
    Настройка отображения записей на обслуживание в административной панели.
    """
    list_display = ('user_full_name', 'user_phone_number', 'car_model', 'service_date', 'service_time', 'additional_info')
    search_fields = ('user__username', 'user__email', 'car_model', 'user__phone_number')
    list_filter = ('service_date', 'service_time')
    autocomplete_fields = ['user']  # Поле автозаполнения для пользователя

    def user_full_name(self, obj):
        """
        Возвращает полное имя пользователя.
        """
        return f"{obj.user.first_name} {obj.user.last_name}"

    def user_phone_number(self, obj):
        """
        Возвращает номер телефона пользователя.
        """
        return obj.user.phone_number

    user_full_name.short_description = 'Полное имя'
    user_phone_number.short_description = 'Номер телефона'


admin.site.register(ServiceAppointment, ServiceAppointmentAdmin)
