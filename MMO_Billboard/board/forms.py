from django_summernote.widgets import SummernoteWidget

from board.models import *
from django import forms


class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text', 'author', 'post']
        exclude = ['author', 'post']
        labels = {
            "text": "Отклик",
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author']
        widgets = {
            'content': SummernoteWidget()
        }
