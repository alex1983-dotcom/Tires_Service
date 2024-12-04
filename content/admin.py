from django.contrib import admin  # Импортируем модуль админки Django
from .models import DynamicArticle, HomePage  # Импортируем модели DynamicArticle и HomePage из текущего модуля
from .forms import DynamicArticleForm


@admin.register(DynamicArticle)  # Используем декоратор для регистрации модели DynamicArticle в админке
class DynamicArticleAdmin(admin.ModelAdmin):
    """
    Класс для управления моделью DynamicArticle в административной панели.

    Атрибуты:
        form (DynamicArticleForm): Форма, используемая для создания и редактирования статей.
        list_display (tuple): Поля, отображаемые в списке записей в административной панели.
        search_fields (tuple): Поля, по которым можно выполнять поиск в административной панели.
        list_filter (tuple): Поля, по которым можно фильтровать записи в административной панели.
        fields (tuple): Поля, отображаемые в форме создания и редактирования записи.
    """
    form = DynamicArticleForm
    list_display = ('title', 'author', 'created_at', 'rubric')  # Поля, отображаемые в списке записей в административной панели.
    search_fields = ('title', 'author', 'rubric__name')  # Поля, по которым можно выполнять поиск в административной панели.
    list_filter = ('rubric', 'author', 'created_at')  # Поля, по которым можно фильтровать записи в административной панели.
    fields = ('title', 'content', 'author', 'rubric', 'file')  # Поля, отображаемые в форме создания и редактирования записи.


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    """
    Класс для управления моделью HomePage в административной панели.

    Атрибуты:
        list_display (tuple): Поля, отображаемые в списке записей в административной панели.
        search_fields (tuple): Поля, по которым можно выполнять поиск в административной панели.
    """
    list_display = ('title', 'address', 'phone', 'unp', 'legal_address')  # Поля, отображаемые в списке записей в административной панели.
    search_fields = ('title', 'address', 'phone', 'unp', 'legal_address')  # Поля, по которым можно выполнять поиск в административной панели.


