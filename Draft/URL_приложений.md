`user_registration\urls`
```
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, personal_cabinet, book_service, login_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('personal_cabinet/', personal_cabinet, name='personal_cabinet'),
    path('book_service/', book_service, name='book_service'),
]
```


`content\urls`
```
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import HomePageView, CategoryArticlesView, ArticleDetailView

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('category/<int:pk>/', CategoryArticlesView.as_view(), name='category_articles'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='dynamic_article_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

