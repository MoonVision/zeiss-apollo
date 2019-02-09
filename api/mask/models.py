from django.db import models
from django.utils import timezone

from image.models import Image


class Ellipse(models.Model):
    centerX = models.PositiveIntegerField()
    centerY = models.PositiveIntegerField()
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    rotation = models.FloatField()


class Mask(models.Model):
    create_time = models.DateTimeField(default=timezone.now)


class Position(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    images = models.ManyToManyField(Image, through='PositionImage')


class PositionImage(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    postition = models.ForeignKey(Position, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)


class Defect(models.Model):
    position_image = models.ForeignKey(PositionImage, on_delete=models.CASCADE)
    elipse = models.ForeignKey(Ellipse, on_delete=models.CASCADE)
