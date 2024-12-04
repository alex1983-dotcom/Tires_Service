from django import forms
from .models import DynamicArticle
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class DynamicArticleForm(forms.ModelForm):
    """
    Форма для модели DynamicArticle.

    Класс Meta:
        model: Указывает, что данная форма работает с моделью DynamicArticle.
        fields: Перечисляет поля модели, которые будут доступны в форме.
    """

    class Meta:
        model = DynamicArticle
        fields = ['title', 'content', 'author', 'rubric', 'file']

    def clean(self):
        """
        Метод для валидации данных формы.

        Проверяет, что заголовок статьи не пустой.

        Raises:
            ValidationError: Если заголовок статьи пустой.

        Returns:
            dict: Очищенные данные формы.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if not title:
            raise ValidationError('Заголовок статьи обязателен.')

        return cleaned_data

    def save(self, commit=True):
        """
        Метод для сохранения данных формы с обработкой исключений.

        Args:
            commit (bool): Флаг, указывающий, следует ли немедленно сохранить объект в базу данных. По умолчанию True.

        Raises:
            IntegrityError: Если возникает ошибка целостности базы данных при сохранении статьи.
            Exception: Если возникает любая другая ошибка при сохранении статьи.

        Returns:
            instance: Сохраненный экземпляр модели DynamicArticle.
        """
        try:
            instance = super().save(commit=False)
            if commit:
                instance.save()
            return instance
        except IntegrityError as e:
            self.add_error(None, f'Ошибка сохранения статьи: {e}')
        except Exception as e:
            self.add_error(None, f'Произошла ошибка: {e}')
