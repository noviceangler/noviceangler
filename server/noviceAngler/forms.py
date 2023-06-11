from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['subject', 'content', 'image']
        labels = {
            'subject': '제목',
            'content': '내용', 
            'image' : '이미지',
                  }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글',
        }