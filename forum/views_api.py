from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Thread, Post
from .serializers import CategorySerializer, ThreadSerializer, PostSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для категорий форума.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def retrieve_with_exception_handling(self, request, pk=None):
        """
        Обработчик GET-запросов с обработкой исключений.
        """
        try:
            category = self.get_object()
            serializer = self.get_serializer(category)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response({'error': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Произошла ошибка: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ThreadViewSet(viewsets.ModelViewSet):
    """
    ViewSet для тем обсуждения на форуме.
    """
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer

    @action(detail=True, methods=['get'])
    def retrieve_with_exception_handling(self, request, pk=None):
        """
        Обработчик GET-запросов с обработкой исключений.
        """
        try:
            thread = self.get_object()
            serializer = self.get_serializer(thread)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response({'error': 'Тема не найдена'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Произошла ошибка: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet для сообщений на форуме.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['get'])
    def retrieve_with_exception_handling(self, request, pk=None):
        """
        Обработчик GET-запросов с обработкой исключений.
        """
        try:
            post = self.get_object()
            serializer = self.get_serializer(post)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response({'error': 'Сообщение не найдено'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Произошла ошибка: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        """
        Обработчик POST-запросов для создания сообщения с обработкой исключений.
        """
        try:
            response = super().create(request, *args, **kwargs)
            return response
        except IntegrityError as e:
            return Response({'error': f'Ошибка целостности данных: {e}'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Произошла ошибка: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
