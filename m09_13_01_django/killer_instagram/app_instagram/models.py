import os
from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def update_filename(instance, filename):
    upload_to = f'uploads'
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join(upload_to, filename)


# Create your models here.
class Picture(models.Model):
    description = models.CharField(max_length=150, blank=True)
    path = models.ImageField(upload_to=update_filename)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}({self.user.email}): {self.path}'
