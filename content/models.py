from django.db import models

# Create your models here.
# Create your models here.
from django.db import models

class DynamicArticle(models.Model):
    """
    Этот класс определяет структуру данных для хранения статей в базе данных.
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    rubric = models.CharField(max_length=100, default='Общая')

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