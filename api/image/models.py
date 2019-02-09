from django.db import models
from django.utils import timezone


def image_path(instance, filename):
    return f'images/{uuid.uuid4()}.{filename.split(".")[-1]}'


class Image(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to=image_path, height_field='height', width_field='width')
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
