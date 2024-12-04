from django.contrib import admin
from .models import Order, OrderItem, Product, Category, Cart, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Административная панель для управления моделью Category.
    """
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная панель для управления моделью Product.
    """
    list_display = ['name', 'price', 'category']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Административная панель для управления моделью Cart.
    """
    list_display = ['user__last_name', 'user__first_name', 'user']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Административная панель для управления моделью CartItem.
    """
    list_display = ['cart', 'product', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Административная панель для управления моделью Order.
    """
    list_display = ['id', 'user', 'created_at', 'processed']
    list_filter = ['processed', 'created_at', 'user']
    search_fields = ['user__username', 'id']
    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        """
        Помечает выбранные заказы как обработанные.
        """
        queryset.update(processed=True)
        self.message_user(request, "Выбранные заказы помечены как обработанные")
    mark_as_processed.short_description = "Пометить как обработанные"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Административная панель для управления моделью OrderItem.
    """
    list_display = ['order', 'product', 'quantity', 'price', 'processed']
    list_filter = ['order', 'product', 'processed']
    search_fields = ['order__id', 'product__name']
    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        """
        Помечает выбранные элементы заказа как обработанные.
        """
        queryset.update(processed=True)
        self.message_user(request, "Выбранные элементы заказа помечены как обработанные")
    mark_as_processed.short_description = "Пометить как обработанные"
