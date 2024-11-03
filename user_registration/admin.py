from django.contrib import admin
from .models import User, Discount, TireStorage, ServiceAppointment


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)

admin.site.register(User, UserAdmin)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'user_email', 'total_spent', 'calculate_discount')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('user', 'total_spent')
    raw_id_fields = ('user',)  # Поле автозаполнения для пользователя

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def user_email(self, obj):
        return obj.user.email

    user_full_name.short_description = 'Full Name'
    user_email.short_description = 'Email'

admin.site.register(Discount, DiscountAdmin)

class TireStorageAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'entry_date', 'exit_date', 'calculate_storage_cost')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('user', 'entry_date', 'exit_date')
    autocomplete_fields = ['user']  # Поле автозаполнения для пользователя

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    user_full_name.short_description = 'Full Name'

admin.site.register(TireStorage, TireStorageAdmin)

class ServiceAppointmentAdmin(admin.ModelAdmin):
    """
    Настройка отображения записей на обслуживание в административной панели.
    """
    list_display = ('user_full_name', 'car_model', 'service_date', 'service_time', 'additional_info')
    search_fields = ('user__username', 'user__email', 'car_model')
    list_filter = ('service_date', 'service_time')
    autocomplete_fields = ['user']  # Поле автозаполнения для пользователя

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    user_full_name.short_description = 'Full Name'

admin.site.register(ServiceAppointment, ServiceAppointmentAdmin)
