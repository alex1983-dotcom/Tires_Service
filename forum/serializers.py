from rest_framework import serializers
from .models import Category, Thread, Post

class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.
    """
    class Meta:
        model = Category
        fields = '__all__'

class ThreadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Thread.
    """
    class Meta:
        model = Thread
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Post.
    """
    class Meta:
        model = Post
        fields = '__all__'
