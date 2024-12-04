from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Модель, представляющая категорию товаров.

    Атрибуты:
        name (CharField): Название категории.
        description (TextField): Описание категории товара.
    """
    name = models.CharField(max_length=100, help_text="Название категории")
    description = models.TextField(blank=True, help_text="Описание категории товара")

    def __str__(self):
        """
        Возвращает строковое представление объекта категории.

        Returns:
            str: Название категории.
        """
        return self.name


class Product(models.Model):
    """
    Модель, представляющая товар.

    Атрибуты:
        sku (CharField): Артикул товара.
        name (CharField): Название товара.
        description (TextField): Описание товара.
        price (DecimalField): Цена товара.
        image (ImageField): Фото товара.
        category (ForeignKey): Категория товара.
    """
    sku = models.CharField(max_length=50, unique=True, help_text="Артикул товара")
    name = models.CharField(max_length=100, help_text="Название товара")
    description = models.TextField(help_text="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Цена товара")
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Фото товара")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, help_text="Категория товара")

    def __str__(self):
        """
        Возвращает строковое представление объекта товара.

        Returns:
            str: Название товара.
        """
        return self.name


class Cart(models.Model):
    """
    Модель, представляющая корзину заказов.

    Атрибуты:
        user (ForeignKey): Пользователь, владелец корзины.
        created_at (DateTimeField): Дата и время создания корзины.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Возвращает строковое представление объекта корзины.

        Returns:
            str: Описание корзины с указанием пользователя и даты создания.
        """
        return f"Корзина пользователя {self.user.username} от {self.created_at}"


class CartItem(models.Model):
    """
    Модель, представляющая элемент корзины.

    Атрибуты:
        cart (ForeignKey): Корзина, к которой относится элемент.
        product (ForeignKey): Товар, добавленный в корзину.
        quantity (PositiveIntegerField): Количество товара.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """
        Возвращает строковое представление объекта элемента корзины.

        Returns:
            str: Описание элемента корзины с указанием товара и количества.
        """
        return f"{self.product.name} (x{self.quantity})"


class Order(models.Model):
    """
    Модель, представляющая заказ.

    Атрибуты:
        user (ForeignKey): Пользователь, который сделал заказ.
        cart (ForeignKey): Корзина, на основе которой сделан заказ.
        created_at (DateTimeField): Дата и время создания заказа.
        processed (BooleanField): Статус обработки заказа.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def __str__(self):
        """
        Возвращает строковое представление объекта заказа.

        Returns:
            str: Описание заказа с указанием его ID, пользователя и даты создания.
        """
        return f"Заказ {self.id} пользователя {self.user.username} от {self.created_at}"


class OrderItem(models.Model):
    """
    Модель, представляющая элемент заказа.

    Атрибуты:
        order (ForeignKey): Заказ, к которому относится элемент.
        product (ForeignKey): Товар, входящий в заказ.
        quantity (PositiveIntegerField): Количество товара.
        price (DecimalField): Цена товара.
        processed (BooleanField): Статус обработки элемента заказа.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    processed = models.BooleanField(default=False)

    def __str__(self):
        """
        Возвращает строковое представление объекта элемента заказа.

        Returns:
            str: Описание элемента заказа с указанием количества и названия товара.
        """
        return f'{self.quantity} x {self.product.name}'
