from django import forms
from .models import DynamicArticle
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class DynamicArticleForm(forms.ModelForm):
    class Meta:
        model = DynamicArticle
        fields = ['title', 'content', 'author', 'rubric', 'file']

    def clean(self):
        """
        Метод для валидации данных формы.
        """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        if not title:
            raise ValidationError('Заголовок статьи обязателен.')

        return cleaned_data

    def save(self, commit=True):
        """
        Метод для сохранения данных формы с обработкой исключений.
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
