from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Thread, Post

class HomePageView(View):
    """
    Представление для главной страницы форума.
    """
    template_name = 'forum/home_page_forum.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CategoryListView(ListView):
    """
    Представление для отображения списка категорий на форуме.
    """
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

class ThreadListView(View):
    """
    Представление для отображения списка тем в категории.
    """
    template_name = 'forum/thread_list.html'

    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        threads = Thread.objects.filter(category=category)
        context = {'category': category, 'threads': threads}
        return render(request, self.template_name, context)

class PostListView(View):
    """
    Представление для отображения списка сообщений в теме.
    """
    template_name = 'forum/post_list.html'

    def get(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(Thread, id=thread_id)
        posts = Post.objects.filter(thread=thread)
        context = {'thread': thread, 'posts': posts}
        return render(request, self.template_name, context)
