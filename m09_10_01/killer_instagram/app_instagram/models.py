import os
from uuid import uuid4

from django.db import models


def update_filename(instance, filename):
    upload_to = 'uploads'
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join(upload_to, filename)


# Create your models here.
class Picture(models.Model):
    description = models.CharField(max_length=150)
    path = models.ImageField(upload_to=update_filename)
