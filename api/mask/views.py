import json

from rest_framework import viewsets
from rest_framework.decorators import action

from mask.models import Mask, DefectPosition, DefectPositionImage, Defect
from mask.serializers import MaskSerializer, DefectPositionSerializer, DefectPositionImageSerializer, DefectSerializer


class MaskViewSet(viewsets.ModelViewSet):
    queryset = Mask.objects.all().order_by('-pk')
    serializer_class = MaskSerializer


class DefectPositionViewSet(viewsets.ModelViewSet):
    queryset = DefectPosition.objects.all().order_by('-pk')
    serializer_class = DefectPositionSerializer

from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser


class DefectPositionImageViewSet(viewsets.ModelViewSet):
    serializer_class = DefectPositionImageSerializer
    parser_classes = (MultiPartParser,)


    def get_queryset(self):
        queryset = DefectPositionImage.objects.all()

        mask = self.request.query_params.get('mask', None)
        if mask is not None:
            queryset = queryset.filter(defect_position__mask=mask)

        return queryset.order_by('-pk')

    def create(self, request, *args, **kwargs):
        print(request.data)
        request.data['new_defects[0]'] = json.loads(request.data['new_defects'])[0]
        print(request.data)
        return super(DefectPositionImageViewSet, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        mask_id = serializer.validated_data.pop('mask_id', None)
        position_x = serializer.validated_data.pop('position_x', None)
        position_y = serializer.validated_data.pop('position_y', None)

        mask = None
        if mask_id:
            if Mask.objects.filter(id=mask_id).exists():
                mask = Mask.objects.get(id=mask_id)
            else:
                mask = Mask()
                mask.save()

        if position_x and position_y and mask:
            if DefectPosition.objects.filter(x=position_x, y=position_y, mask=mask).exists():
                detect_position = DefectPosition.objects.get(x=position_x, y=position_y, mask=mask)
            else:
                detect_position = DefectPosition(x=position_x, y=position_y, mask=mask)
                detect_position.save()
            serializer.validated_data['defect_position'] = detect_position

        serializer.save()


class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all().order_by('-pk')
    serializer_class = DefectSerializer
