from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import HomePageView, CategoryArticlesView, ArticleDetailView
from django.shortcuts import render


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('category/<int:pk>/', CategoryArticlesView.as_view(), name='category_articles'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='dynamic_article_detail'),
    path('error/', lambda request: render(request, 'content/error.html'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
