from django.contrib import admin
from .models import DynamicArticle

class DynamicArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'rubric')
    search_fields = ('title', 'author', 'rubric__name')
    list_filter = ('rubric', 'author', 'created_at')  # Фильтры для рубрик, авторов и даты создания
    fields = ('title', 'content', 'author', 'rubric')

admin.site.register(DynamicArticle, DynamicArticleAdmin)


