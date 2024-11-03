from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    """
    Класс менеджера для пользователей, который обеспечивает создание
    обычных пользователей и суперпользователей.
    """
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Пользователи должны иметь email адрес')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """
    Класс модели пользователя, который расширяет AbstractBaseUser и PermissionsMixin.
    Содержит поля для фамилии, имени, отчества, email, имени пользователя и другие необходимые поля.
    """
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='user_registration_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='user_registration_user_permissions')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.email})"

class Discount(models.Model):
    """
    Класс модели скидок, который хранит информацию о накопленных бонусах и проценте скидки.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)

    def calculate_discount(self):
        """
        Рассчитывает процент скидки на основе накопленных бонусов.
        """
        bonus_discount = self.total_spent * self.discount_rate
        return bonus_discount

    def update_total_spent(self, amount):
        """
        Обновляет общую потраченную сумму (накопленные бонусы).
        """
        self.total_spent += amount
        self.save()

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"

    def __str__(self):
        return f"Скидка для {self.user.username}: {self.calculate_discount()}%"
