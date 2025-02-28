from django import forms
from django_filters import FilterSet, ModelChoiceFilter
from .models import Reply, Post


class ReplyFilter(FilterSet):
    post__title = ModelChoiceFilter(
        label='Название объявления',
        queryset=None,
        widget=forms.Select,
        empty_label='Все отклики'
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.filters['post__title'].queryset = Post.objects.filter(author=user)
        if not self.data.get('post__title'):
            self.queryset = Reply.objects.filter(post__author=user)