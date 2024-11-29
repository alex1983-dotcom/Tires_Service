from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Административная панель для управления категориями товаров.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Административная панель для управления товарами.
    """
    list_display = ('name', 'sku', 'category', 'price')
    search_fields = ('name', 'sku')
    list_filter = ('category',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """
    Административная панель для управления корзинами.
    """
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'user__email')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """
    Административная панель для управления элементами корзины.
    """
    list_display = ('cart', 'product', 'quantity')
    search_fields = ('cart__user__username', 'product__name')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Административная панель для управления заказами.
    """
    list_display = ('user', 'created_at', 'processed')
    search_fields = ('user__username', 'user__email')
    list_filter = ('processed',)
