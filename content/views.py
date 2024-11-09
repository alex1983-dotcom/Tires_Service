from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import DynamicArticle, HomePage
import markdown
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.conf import settings


def markdown_to_html(text):
    return markdown.markdown(text)


class HomePageView(View):
    """
    Этот контроллер отвечает за отображение главной страницы.
    """
    def get(self, request):
        """
        Выполняет GET-запрос для отображения главной страницы.
        """
        home_page = get_object_or_404(HomePage, id=1)
        categories = DynamicArticle.objects.values('rubric').distinct()
        categories_with_ids = [{"id": i, "name": c['rubric']} for i, c in enumerate(categories)]
        context = {
            'home_page': home_page,
            'categories': categories_with_ids,
            'MEDIA_URL': settings.MEDIA_URL
        }
        return render(request, 'content/home_page.html', context)

class CategoryArticlesView(View):
    """
    Отображение статей в определенной категории.
    """
    def get(self, request, pk):
        """
        Выполняет GET-запрос для отображения статей в категории.
        """
        category_name = DynamicArticle.objects.values_list('rubric', flat=True).distinct()[pk]
        articles = DynamicArticle.objects.filter(rubric=category_name)
        context = {
            'category': {'name': category_name},
            'articles': articles
        }
        return render(request, 'content/category_articles.html', context)

class ArticleDetailView(View):
    """
    Отображение деталей статьи на странице.
    """
    @method_decorator(never_cache)
    def get(self, request, pk):
        article = get_object_or_404(DynamicArticle, pk=pk)
        categories = DynamicArticle.objects.values('rubric').distinct()
        categories_with_ids = [{"id": i, "name": c['rubric']} for i, c in enumerate(categories)]
        article_content_html = markdown_to_html(article.content)
        context = {
            'article': article,
            'article_content_html': article_content_html,
            'categories': categories_with_ids
        }
        return render(request, 'content/article_detail.html', context)
