from django.contrib import admin
from .models import Category, Thread, Post


class ThreadAdmin(admin.ModelAdmin):
    """
    Административная панель для управления темами на форуме.
    """
    list_display = ('title', 'category', 'created_by', 'created_at')
    search_fields = ('title', 'category__name', 'created_by__username')


class PostAdmin(admin.ModelAdmin):
    """
    Административная панель для управления сообщениями на форуме.
    """
    list_display = ('thread', 'created_by', 'created_at')
    search_fields = ('thread__title', 'created_by__username')


# Регистрация моделей в админке для управления через административную панель
admin.site.register(Category)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)


