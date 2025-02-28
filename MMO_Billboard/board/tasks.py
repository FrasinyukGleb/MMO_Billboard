from celery import shared_task
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post
from django.contrib.auth.models import User


@shared_task
def daily_email_notification():
    today = datetime.datetime.now()
    last_day = today - datetime.timedelta(days=1)
    posts = Post.objects.filter(date__gte=last_day)
    users = User.objects.all()

    emails = set(users.values_list('email', flat=True))

    html_content = render_to_string(
            'board/daily_post.html',
            {
                'link': 'http://127.0.0.1:8000/',
                'posts': posts,
            }
        )

    msg = EmailMultiAlternatives(
            subject='Объявления за день',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=emails
        )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#celery -A MMO_Billboard worker --loglevel=info -P eventlet  --pool=solo
#celery -A MMO_Billboard beat --loglevel=info
