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
    serializer_class = DefectPositionImageSerializer

    def get_queryset(self):
        queryset = DefectPositionImage.objects.all()

        mask = self.request.query_params.get('mask', None)
        if mask is not None:
            queryset = queryset.filter(defect_position__mask=mask)

        return queryset

class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
