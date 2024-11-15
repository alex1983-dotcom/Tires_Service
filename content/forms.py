from django import forms
from .models import DynamicArticle


class DynamicArticleForm(forms.ModelForm):
    class Meta:
        model = DynamicArticle
        fields = ['title', 'content', 'author', 'rubric', 'file']
