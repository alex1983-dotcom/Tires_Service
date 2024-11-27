from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

class UserManager(BaseUserManager):
    def create_user(self, phone_number, username, middle_name=None, email=None, password=None):
        if not phone_number:
            raise ValueError('Пользователи должны иметь номер телефона')
        user = self.model(
            phone_number=phone_number,
            username=username,
            middle_name=middle_name,
            email=self.normalize_email(email) if email else None,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, username='admin', middle_name=None):
        if not email:
            raise ValueError('Суперпользователи должны иметь электронную почту')
        if not phone_number:
            raise ValueError('Суперпользователи должны иметь номер телефона')
        user = self.create_user(
            phone_number=phone_number,
            email=email,
            password=password,
            username=username,
            middle_name=middle_name,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    groups = models.ManyToManyField(Group, related_name='user_registration_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='user_registration_user_permissions', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'username']

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        """
        Возвращает полное имя пользователя.
        """
        return f"{self.first_name} {self.middle_name} {self.last_name}".strip()

    def get_short_name(self):
        """
        Возвращает краткое имя пользователя.
        """
        return self.first_name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

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


class TireStorage(models.Model):
    """
    Класс модели для хранения информации о шинах.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry_date = models.DateField()
    exit_date = models.DateField(null=True, blank=True)
    daily_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)
    tire_model = models.CharField(max_length=50, default='Неизвестная модель')  # Поле для модели шины с значением по умолчанию
    tire_size = models.CharField(max_length=20, default='Неизвестный размер')   # Поле для размера шины с значением по умолчанию
    quantity = models.CharField(max_length=2, default='Неизвестное количество')

    def calculate_storage_cost(self):
        from datetime import date
        days_stored = (self.exit_date or date.today()) - self.entry_date
        return days_stored.days * self.daily_rate

    class Meta:
        verbose_name = "Хранение шины"
        verbose_name_plural = "Хранение шин"

    def __str__(self):
        return f"Хранение шины для {self.user.username}: {self.calculate_storage_cost()}р"


class ServiceAppointment(models.Model):
    """
    Класс модели для записи клиентов на обслуживание.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_model = models.CharField(max_length=50)
    service_date = models.DateField()
    service_time = models.TimeField()
    additional_info = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Запись на обслуживание"
        verbose_name_plural = "Записи на обслуживание"

    def __str__(self):
        return f"Запись на {self.service_date} {self.service_time} для {self.user.username}"

from django.db import models
from django.utils import timezone

class PasswordResetCode(models.Model):
    phone_number = models.CharField(max_length=15)  # Номер телефона пользователя
    code = models.CharField(max_length=6)  # Код сброса пароля
    expiry_date = models.DateTimeField()  # Срок действия кода

    def is_valid(self):
        """
        Проверяет, действителен ли код сброса пароля.
        """
        return self.expiry_date >= timezone.now()

    def __str__(self):
        return f"Password reset code for {self.phone_number}"

