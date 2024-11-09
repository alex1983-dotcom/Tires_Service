from django.contrib import admin  # Импортируем модуль админки Django
from .models import DynamicArticle, HomePage  # Импортируем модели DynamicArticle и HomePage из текущего модуля

@admin.register(DynamicArticle)  # Используем декоратор для регистрации модели DynamicArticle в админке
class DynamicArticleAdmin(admin.ModelAdmin):  # Определяем класс для админской панели модели DynamicArticle, наследуемся от admin.ModelAdmin

    # Указываем поля, которые будут отображаться в списке записей в админке
    list_display = ('title', 'author', 'created_at', 'rubric')
    # Задаем поля, по которым можно будет выполнять поиск в админке
    search_fields = ('title', 'author', 'rubric__name')
    # Добавляем фильтры для рубрик, авторов и даты создания
    list_filter = ('rubric', 'author', 'created_at')
    # Определяем порядок и список полей для формы редактирования
    fields = ('title', 'content', 'author', 'rubric')

@admin.register(HomePage)  # Используем декоратор для регистрации модели HomePage в админке
class HomePageAdmin(admin.ModelAdmin):  # Определяем класс для админской панели модели HomePage, наследуемся от admin.ModelAdmin
    list_display = ('title', 'address', 'phone', 'unp', 'legal_address')  # Указываем поля, которые будут отображаться в списке записей в админке
    search_fields = ('title', 'address', 'phone', 'unp', 'legal_address')  # Задаем поля, по которым можно будет выполнять поиск в админке


