from django.db import models
from django.utils import timezone

from image.models import Image


class Mask(models.Model):
    create_time = models.DateTimeField(default=timezone.now)


class DefectPosition(models.Model):
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    create_time = models.DateTimeField(default=timezone.now)
    mask = models.ForeignKey(Mask, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('mask', 'x', 'y')

class DefectPositionImage(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    defect_position = models.ForeignKey(DefectPosition, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def get_defects(self):
        return Defect.objects.filter(position_image=self)


class Ellipse(models.Model):
    centerX = models.PositiveIntegerField()
    centerY = models.PositiveIntegerField()
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    rotation = models.FloatField()


class Defect(models.Model):
    position_image = models.ForeignKey(DefectPositionImage, on_delete=models.CASCADE)
    ellipse = models.ForeignKey(Ellipse, on_delete=models.CASCADE)
