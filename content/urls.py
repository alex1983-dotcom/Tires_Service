from django.urls import path
from .views import HomePageView, CategoryArticlesView, ArticleDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('category/<int:pk>/', CategoryArticlesView.as_view(), name='category_articles'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='dynamic_article_detail'),
]