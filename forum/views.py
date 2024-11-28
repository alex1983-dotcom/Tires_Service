from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Category, Thread, Post
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class HomePageView(View):
    template_name = 'forum/home_page_forum.html'

    def get(self, request, *args, **kwargs):
        try:
            return render(request, self.template_name)
        except Exception as e:
            # Логирование ошибки
            print(f"Ошибка загрузки домашней страницы: {e}")
            return render(request, 'forum/error.html', {'error_message': 'Не удалось загрузить домашнюю страницу'})


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        try:
            return Category.objects.all()
        except Exception as e:
            # Логирование ошибки
            print(f"Ошибка загрузки списка категорий: {e}")
            return []


class ThreadListView(LoginRequiredMixin, View):
    template_name = 'forum/thread_list.html'

    def get(self, request, category_id, *args, **kwargs):
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
    template_name = 'forum/post_list.html'

    def get(self, request, thread_id, *args, **kwargs):
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
    return render(request, 'forum/error.html', {'error_message': 'Произошла ошибка'})
