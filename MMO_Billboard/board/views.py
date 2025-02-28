from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from board.forms import *
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from board.models import *
from board.filters import ReplyFilter


class ReplyList(LoginRequiredMixin, ListView):
    model = Reply
    ordering = '-date'
    context_object_name = 'replies'
    paginate_by = 10
    template_name = 'account/account.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ReplyFilter(self.request.GET, queryset, user=self.request.user)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


def reply_delete(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()
    return redirect('account')


def reply_accept(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.accepted = True
    reply.save()

    message = f"Ваше предложение '{reply}' на пост '{reply.post}' приняли! \n" \
              f"Связаться с автором Вы можете по почте: {reply.post.author.email}"

    send_mail(
        f'Ваше предложение приняли!',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [reply.author.email],
    )
    return redirect('account')


class PostsList(ListView):
    model = Post
    ordering = '-date'
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'board/home.html'


class AccountPostsList(ListView):
    model = Post
    ordering = '-date'
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'board/post_list.html'

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)
        return queryset


class PostDetail(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'board/post_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post

    def get_template_names(self):
        return 'board/post_create.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('account')

    def get_template_names(self):
        return 'board/post_delete.html'


class ReplyCreate(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'board/reply_create.html'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.author = self.request.user
        reply.post = Post.objects.get(pk=self.request.path.split('/')[2])
        reply.save()
        return super().form_valid(form)

# Вызовется так же, если в функции будет: raise Http404()
def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

