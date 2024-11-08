from django.contrib import admin
from user_registration.models import User, Discount, TireStorage, ServiceAppointment

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('email',)

admin.site.register(User, UserAdmin)

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'user_email', 'user_phone_number', 'total_spent', 'calculate_discount')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'user__phone_number')
    list_filter = ('user', 'total_spent')
    raw_id_fields = ('user',)  # Поле автозаполнения для пользователя

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def user_email(self, obj):
        return obj.user.email

    def user_phone_number(self, obj):
        return obj.user.phone_number

    user_full_name.short_description = 'Full Name'
    user_email.short_description = 'Email'
    user_phone_number.short_description = 'Phone Number'

admin.site.register(Discount, DiscountAdmin)

class TireStorageAdmin(admin.ModelAdmin):
    list_display = ('user_full_name', 'user_phone_number', 'entry_date', 'exit_date', 'calculate_storage_cost')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'user__phone_number')
    list_filter = ('user', 'entry_date', 'exit_date')
    autocomplete_fields = ['user']  # Поле автозаполнения для пользователя

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def user_phone_number(self, obj):
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
        return f"{obj.user.first_name} {obj.user.last_name}"

    def user_phone_number(self, obj):
        return obj.user.phone_number

    user_full_name.short_description = 'Full Name'
    user_phone_number.short_description = 'Phone Number'

admin.site.register(ServiceAppointment, ServiceAppointmentAdmin)
