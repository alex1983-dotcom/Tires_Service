from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Category, Thread, Post
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePageView(View):
    template_name = 'forum/home_page_forum.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

class ThreadListView(LoginRequiredMixin, View):
    template_name = 'forum/thread_list.html'

    def get(self, request, category_id, *args, **kwargs):
        category = get_object_or_404(Category, id=category_id)
        threads = Thread.objects.filter(category=category)
        context = {'category': category, 'threads': threads}
        return render(request, self.template_name, context)


class PostListView(View):
    template_name = 'forum/post_list.html'

    def get(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(Thread, id=thread_id)
        posts = Post.objects.filter(thread=thread)
        context = {'thread': thread, 'posts': posts}
        return render(request, self.template_name, context)

    def post(self, request, thread_id, *args, **kwargs):
        thread = get_object_or_404(Thread, id=thread_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
        parent = Post.objects.get(id=parent_id) if parent_id else None
        if content:
            Post.objects.create(thread=thread, created_by=request.user, message=content, parent=parent)
        return redirect('post_list', thread_id=thread.id)

