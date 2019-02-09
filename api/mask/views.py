from rest_framework import viewsets

from mask.models import Mask, DefectPosition, DefectPositionImage, Defect
from mask.serializers import MaskSerializer, DefectPositionSerializer, DefectPositionImageSerializer, DefectSerializer


class MaskViewSet(viewsets.ModelViewSet):
    queryset = Mask.objects.all()
    serializer_class = MaskSerializer


class DefectPositionViewSet(viewsets.ModelViewSet):
    queryset = DefectPosition.objects.all()
    serializer_class = DefectPositionSerializer


class DefectPositionImageViewSet(viewsets.ModelViewSet):
    queryset = DefectPositionImage.objects.all()
    serializer_class = DefectPositionImageSerializer


class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
