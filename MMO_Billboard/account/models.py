from django.db import models
from django.contrib.auth.models import User


class OneTimeCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return self.code
