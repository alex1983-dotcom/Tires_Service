from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для категории товаров.
    """
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для товаров.
    """
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для элементов корзины
    """
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    """
    Сериализатор для корзины заказов.
    """
    items = CartItemSerializer(many=True, read_only=True)

    class Mete:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items']


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для заказов.
    """
    class Meta:
        model = Order
        fields = '__all__'

