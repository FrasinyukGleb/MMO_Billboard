from django.urls import path
from board.views import *

urlpatterns = [
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/reply', ReplyCreate.as_view(), name='reply_create'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/update', PostUpdate.as_view(), name='post_update'),
    path('', AccountPostsList.as_view(), name='post_list'),
    path('reply/<int:pk>/delete', reply_delete, name='reply_delete'),
    path('reply/<int:pk>/accept', reply_accept, name='reply_accept'),
]