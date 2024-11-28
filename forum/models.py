from django.db import models, IntegrityError
from django.conf import settings


class Category(models.Model):
    """
    Модель для представления категории на форуме.
    """
    name = models.CharField(max_length=100, help_text="Название категории")
    description = models.TextField(help_text="Описание категории")

    def __str__(self):
        """
        Возвращает строковое представление категории.
        """
        return f"Категория: {self.name}"


class Thread(models.Model):
    """
    Модель для представления темы обсуждения на форуме.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Категория, к которой относится тема")
    title = models.CharField(max_length=200, help_text="Название темы")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   help_text="Пользователь, создавший тему")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания темы")

    def __str__(self):
        """
        Возвращает строковое представление темы.
        """
        return f"Тема: {self.title} (Создано: {self.created_at})"


class Post(models.Model):
    """
    Модель для представления сообщения в теме обсуждения на форуме.
    """
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, help_text="Тема, к которой относится сообщение")
    message = models.TextField(help_text="Текст сообщения")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   help_text="Пользователь, создавший сообщение")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания сообщения")
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE,
                               help_text="Родительское сообщение, если это ответ")

    def __str__(self):
        """
        Возвращает строковое представление сообщения.
        """
        return f"Сообщение от {self.created_by} в {self.created_at}"

    @classmethod
    def create_post(cls, thread, message, created_by, parent=None):
        try:
            post = cls(thread=thread, message=message, created_by=created_by, parent=parent)
            post.save()
            return post
        except IntegrityError as e:
            print(f"Ошибка создания сообщения: {e}")
            return None
