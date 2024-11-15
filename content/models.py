# Create your models here.
# Create your models here.
from django.db import models

class DynamicArticle(models.Model):
    """
    Этот класс определяет структуру данных для хранения статей в базе данных.
    """
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    rubric = models.CharField(max_length=100, default='Общая')
    file = models.FileField(upload_to='my_articles/', blank=True,null=True)

    def save(self, *args, **kwargs):
        if self.file:
            # Чтение содержимого файла и сохранение его в поле content
            self.content = self.file.read().decode('utf-8')  # Декодируем, если это текстовый файл
        super().save(*args, **kwargs)

    @property
    def content_html(self):
        """
        Этот метод берет содержимое статьи в формате Markdown и возвращает его
        в виде HTML, готового для отображение на веб-странице.
        """
        import markdown
        return markdown.markdown(self.content, extensions=['markdown.extensions.extra'])

class HomePage(models.Model):
    title = models.CharField(max_length=100, default='ProffShina')
    content = models.TextField(default='Добро пожаловать на сайт ProffShina.')
    address = models.CharField(max_length=255, default='Адрес предприятия')
    phone = models.CharField(max_length=50, default='Телефон')
    unp = models.CharField(max_length=50, default='УНП')
    legal_address = models.CharField(max_length=255, default='Юридический адрес')