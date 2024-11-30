from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Модель для категории товаров.
    """
    name = models.CharField(max_length=100, help_text="Название категории")
    description = models.TextField(blank=True, help_text="Описание категории товара")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Модель для товаров.
    """
    sku = models.CharField(max_length=50, unique=True, help_text="Артикул товара")
    name = models.CharField(max_length=100, help_text="Название товара")
    description = models.TextField(help_text="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Цена товара")
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Фото товара")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, help_text="Категория товара")

    def __str__(self):
        return self.name


class Cart(models.Model):
    """
    Модель для корзины заказов.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина пользователя {self.user.username} от {self.created_at}"


class CartItem(models.Model):
    """
    Модель для элементов корзины.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"


class Order(models.Model):
    """
    Модель для заказов.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Заказ {self.id} пользователя {self.user.username} от {self.created_at}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'
























