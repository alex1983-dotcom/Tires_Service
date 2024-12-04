from django.db import models
import markdown

class DynamicArticle(models.Model):
    """
    Этот класс определяет структуру данных для хранения статей в базе данных.
    """
    title = models.CharField(max_length=100, help_text='Заголовок статьи')
    content = models.TextField(blank=True, help_text='Содержимое статьи')
    author = models.CharField(max_length=50, help_text='Автор статьи')
    created_at = models.DateTimeField(auto_now_add=True, help_text='Дата и время создания статьи')
    rubric = models.CharField(max_length=100, default='Общая', help_text='Рубрика статьи')
    file = models.FileField(upload_to='my_articles/', blank=True, null=True, help_text='Файл с содержимым статьи')

    def save(self, *args, **kwargs):
        """
        Переопределенный метод save для сохранения содержимого файла в поле content.

        Args:
            *args: Дополнительные аргументы.
            **kwargs: Дополнительные именованные аргументы.
        """
        try:
            if self.file:
                # Чтение содержимого файла и сохранение его в поле content
                self.content = self.file.read().decode('utf-8')  # Декодируем, если это текстовый файл
        except (FileNotFoundError, UnicodeDecodeError) as e:
            print(f"Ошибка при чтении файла: {e}")
        super().save(*args, **kwargs)

    @property
    def content_html(self):
        """
        Этот метод берет содержимое статьи в формате Markdown и возвращает его
        в виде HTML, готового для отображение на веб-странице.

        Returns:
            str: Содержимое статьи в формате HTML.
        """
        return markdown.markdown(self.content, extensions=['markdown.extensions.extra'])


class HomePage(models.Model):
    """
    Класс для хранения информации о главной странице сайта.
    """
    title = models.CharField(max_length=100, default='ProffShina', help_text='Название сайта')
    content = models.TextField(default='Добро пожаловать на сайт ProffShina.', help_text='Основное содержимое главной страницы')
    address = models.CharField(max_length=255, default='Адрес предприятия', help_text='Адрес предприятия')
    phone = models.CharField(max_length=50, default='Телефон', help_text='Контактный телефон')
    unp = models.CharField(max_length=50, default='УНП', help_text='УНП предприятия')
    legal_address = models.CharField(max_length=255, default='Юридический адрес', help_text='Юридический адрес предприятия')
