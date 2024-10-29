from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Discount

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_spent', 'bonus_points', 'discount_rate')
    search_fields = ('user__username',)
    list_filter = ('user', 'total_spent')

admin.site.register(Discount, DiscountAdmin)
