from django.db import models

# Create your models here.
class User(models.Model):
    """
    Модель для регистрации пользователя
    """
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    username = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email})"


from django.db import models

class Discount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    bonus_points = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Накопительные бонусные баллы
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)  # Процент скидки

    def calculate_discount(self):
        """
        Рассчитывает процент скидки на основе накопленных бонусов.
        """
        bonus_discount = self.bonus_points * 0.15 / 100  # 1 бонусный балл = 0.15%
        return bonus_discount  # Возвращаем процент скидки

    def update_total_spent(self, amount):
        """
        Обновляет общую потраченную сумму и бонусные баллы.
        """
        self.total_spent += amount
        self.bonus_points += amount  # 1 рубль = 1 бонусный балл
        self.save()

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"Скидка для {self.user.username}"
