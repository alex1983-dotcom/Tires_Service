from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Category, Thread, Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class HomePageView(View):
    """
    Представление для отображения домашней страницы форума.

    Атрибуты:
        template_name (str): Имя шаблона, который будет использоваться для отображения домашней страницы.
    """
    template_name = 'forum/home_page_forum.html'

    def get(self, request, *args, **kwargs):
        """
        Обрабатывает GET-запрос для отображения домашней страницы.

        Args:
            request (HttpRequest): Объект запроса.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Ответ с шаблоном домашней страницы.
        """
        try:
            return render(request, self.template_name)
        except Exception as e:
            # Логирование ошибки
            print(f"Ошибка загрузки домашней страницы: {e}")
            return render(request, 'forum/error.html', {'error_message': 'Не удалось загрузить домашнюю страницу'})


class CategoryListView(LoginRequiredMixin, ListView):
    """
    Представление для отображения списка категорий.

    Атрибуты:
        model (Model): Модель, данные которой будут использоваться в представлении.
        template_name (str): Имя шаблона, который будет использоваться для отображения списка категорий.
        context_object_name (str): Имя переменной контекста, которая будет использоваться в шаблоне.
    """
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        """
        Получает набор данных категорий.

        Returns:
            QuerySet: Набор данных категорий.
        """
        try:
            return Category.objects.all()
        except Exception as e:
            # Логирование ошибки
            print(f"Ошибка загрузки списка категорий: {e}")
            return []


class ThreadListView(LoginRequiredMixin, View):
    """
    Представление для отображения списка тем в определенной категории.

    Атрибуты:
        template_name (str): Имя шаблона, который будет использоваться для отображения списка тем.
    """
    template_name = 'forum/thread_list.html'

    def get(self, request, category_id, *args, **kwargs):
        """
        Обрабатывает GET-запрос для отображения списка тем в категории.

        Args:
            request (HttpRequest): Объект запроса.
            category_id (int): Идентификатор категории.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Ответ с шаблоном списка тем.
        """
        try:
            category = get_object_or_404(Category, id=category_id)
            threads = Thread.objects.filter(category=category)
            context = {'category': category, 'threads': threads}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist as e:
            # Логирование ошибки
            print(f"Категория не найдена: {e}")
            return render(request, 'forum/error.html', {'error_message': 'Категория не найдена'})
        except Exception as e:
            # Логирование ошибки
            print(f"Ошибка загрузки списка тем: {e}")
            return render(request, 'forum/error.html', {'error_message': 'Не удалось загрузить список тем'})


class PostListView(View):
    """
    Представление для отображения списка сообщений в теме.

    Атрибуты:
        template_name (str): Имя шаблона, который будет использоваться для отображения списка сообщений.
    """
    template_name = 'forum/post_list.html'

    def get(self, request, thread_id, *args, **kwargs):
        """
        Обрабатывает GET-запрос для отображения списка сообщений в теме.

        Args:
            request (HttpRequest): Объект запроса.
            thread_id (int): Идентификатор темы.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Ответ с шаблоном списка сообщений.
        """
        try:
            thread = get_object_or_404(Thread, id=thread_id)
            posts = Post.objects.filter(thread=thread)
            context = {'thread': thread, 'posts': posts}
            return render(request, self.template_name, context)
        except ObjectDoesNotExist as e:
            # Логирование ошибки
            print(f"Тема не найдена: {e}")
            return render(request, 'forum/error.html', {'error_message': 'Тема не найдена'})
        except Exception as e:
            # Логирование ошибки
            print(f"Ошибка загрузки списка сообщений: {e}")
            return render(request, 'forum/error.html', {'error_message': 'Не удалось загрузить список сообщений'})

    def post(self, request, thread_id, *args, **kwargs):
        """
        Обрабатывает POST-запрос для создания нового сообщения в теме.

        Args:
            request (HttpRequest): Объект запроса.
            thread_id (int): Идентификатор темы.
            *args: Дополнительные позиционные аргументы.
            **kwargs: Дополнительные именованные аргументы.

        Returns:
            HttpResponse: Перенаправление на список сообщений в теме или страница ошибки.
        """
        try:
            thread = get_object_or_404(Thread, id=thread_id)
            content = request.POST.get('content')
            parent_id = request.POST.get('parent_id')
            parent = Post.objects.get(id=parent_id) if parent_id else None
            if content:
                Post.objects.create(thread=thread, created_by=request.user, message=content, parent=parent)
            return redirect('post_list', thread_id=thread.id)
        except ObjectDoesNotExist as e:
            # Логирование ошибки
            print(f"Ошибка создания сообщения: {e}")
            return render(request, 'forum/error.html', {'error_message': 'Не удалось создать сообщение'})
        except IntegrityError as e:
            # Логирование ошибки
            print(f"Ошибка целостности данных при создании сообщения: {e}")
            return render(request, 'forum/error.html', {'error_message': 'Не удалось создать сообщение из-за ошибки целостности данных'})
        except Exception as e:
            # Логирование ошибки
            print(f"Общая ошибка при создании сообщения: {e}")
            return render(request, 'forum/error.html', {'error_message': 'Не удалось создать сообщение'})


def error_view(request):
    """
    Представление для отображения страницы ошибки.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        HttpResponse: Ответ с шаблоном страницы ошибки.
    """
    return render(request, 'forum/error.html', {'error_message': 'Произошла ошибка'})
