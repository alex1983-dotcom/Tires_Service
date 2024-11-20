from django.urls import path
from .views import HomePageView, CategoryListView, ThreadListView, PostListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),  # Маршрут для списка категорий
    path('category/<int:category_id>/threads/', ThreadListView.as_view(), name='thread_list'),  # Маршрут для списка тем в категории
    path('thread/<int:thread_id>/posts/', PostListView.as_view(), name='post_list'),  # Маршрут для списка сообщений в теме
    path('', HomePageView.as_view(), name='forum_home_page'),  # Маршрут для главной страницы форума
]
