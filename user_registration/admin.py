from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Discount

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_spent', 'calculate_discount')  # Добавлен метод calculate_discount
    search_fields = ('user__username',)
    list_filter = ('user', 'total_spent')

    def calculate_discount(self, obj):
        return f"{obj.calculate_discount()}%"

    calculate_discount.short_description = 'Процент скидки'

admin.site.register(Discount, DiscountAdmin)
