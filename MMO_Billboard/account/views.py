from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
import random
import string

from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView

from account.forms import *
from account.models import OneTimeCode
from board.models import Reply
from board.views import ReplyList



def generate_string(length):
    all_symbols = string.ascii_uppercase + string.digits
    result = ''.join(random.choice(all_symbols) for _ in range(length))
    return result


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'account/account.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["posts"] = Post.objects.filter(author=self.request.user).order_by('-date')
    #     return context


class RegisterView(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('onetime_code')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        return super().form_valid(form)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'account/login.html'


def onetime_code(request):
    if request.method == 'POST':
        code = request.POST['code']
        one_time_code = OneTimeCode.objects.filter(code=code)
        if one_time_code:
            user = one_time_code.first().user
            user.is_active = True
            user.save()
            one_time_code.delete()
            return redirect('login')
        else:
            return redirect('code_error')

    return render(request, 'account/onetime_code.html')