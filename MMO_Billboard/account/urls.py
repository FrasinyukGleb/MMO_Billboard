from django.contrib.auth.views import LogoutView
from django.urls import path
from account.views import *
from django.views.generic import TemplateView
from board.views import ReplyList



urlpatterns = [
    path('', ReplyList.as_view(), name='account'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('onetime_code/', onetime_code, name='onetime_code'),
    path('code_error/', TemplateView.as_view(template_name='account/code_error.html'), name='code_error'),
]