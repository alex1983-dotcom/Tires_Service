from django.contrib import admin
from user_registration.models import User, Discount, TireStorage, ServiceAppointment
from django.utils.crypto import get_random_string
from twilio.rest import Client  # Импорт Twilio для отправки SMS


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
        if not change:  # Только при создании нового пользователя
            raw_password = get_random_string(length=8)
            obj.set_password(raw_password)
            obj.save()
            self.send_sms(obj.phone_number, f"Ваш новый пароль: {raw_password}")
        else:
            super().save_model(request, obj, form, change)

    def send_sms(self, phone_number, message):
        """
        Функция для отправки SMS-сообщений с использованием сервиса Twilio.
        """
        account_sid = 'ACed36e0db4aac8d4e6394ed59722b0855'  # Замените на ваш SID аккаунта
        auth_token = '17dc23687e36b441548676998d1107c6'  # Замените на ваш токен аутентификации
        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_='+14128378357',  # Ваш номер, зарегистрированный в Twilio
            to=phone_number
        )


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

    user_full_name.short_description = 'Full Name'
    user_email.short_description = 'Email'
    user_phone_number.short_description = 'Phone Number'


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

    user_full_name.short_description = 'Full Name'
    user_phone_number.short_description = 'Phone Number'


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

    user_full_name.short_description = 'Full Name'
    user_phone_number.short_description = 'Phone Number'


admin.site.register(ServiceAppointment, ServiceAppointmentAdmin)
