from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    CATEGORIES = [('tank', 'Танки'),
                  ('heal', 'Хилы'),
                  ('damager', 'ДД'),
                  ('retailer', 'Торговцы'),
                  ('guildmaster', 'Гилдмастеры'),
                  ('questgiver', 'Квестгиверы'),
                  ('blacksmith', 'Кузнецы'),
                  ('tanner', 'Кожевники'),
                  ('poitionmaster', 'Зельевары'),
                  ('spellmaster', 'Мастера заклинаний')]

    title = models.CharField(verbose_name='Заголовок', max_length=255, null=False)
    author = models.ForeignKey(verbose_name='Автор', to=User, on_delete=models.CASCADE)
    category = models.CharField(verbose_name='Категория', max_length=50, choices=CATEGORIES, default=None)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.pk), ))


class Reply(models.Model):
    author = models.ForeignKey(verbose_name='Автор', to=User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.post.pk), ))
