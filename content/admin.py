from django.contrib import admin  # Импортируем модуль админки Django
from .models import DynamicArticle, HomePage  # Импортируем модели DynamicArticle и HomePage из текущего модуля
from .forms import DynamicArticleForm


@admin.register(DynamicArticle)  # Используем декоратор для регистрации модели DynamicArticle в админке
class DynamicArticleAdmin(admin.ModelAdmin):  # Определяем класс для админской панели модели DynamicArticle, наследуемся от admin.ModelAdmin
    form = DynamicArticleForm
    list_display = ('title', 'author', 'created_at', 'rubric')
    search_fields = ('title', 'author', 'rubric__name')
    list_filter = ('rubric', 'author', 'created_at')
    fields = ('title', 'content', 'author', 'rubric', 'file')


@admin.register(HomePage)  # Используем декоратор для регистрации модели HomePage в админке
class HomePageAdmin(admin.ModelAdmin):  # Определяем класс для админской панели модели HomePage, наследуемся от admin.ModelAdmin
    list_display = ('title', 'address', 'phone', 'unp', 'legal_address')  # Указываем поля, которые будут отображаться в списке записей в админке
    search_fields = ('title', 'address', 'phone', 'unp', 'legal_address')  # Задаем поля, по которым можно будет выполнять поиск в админке


