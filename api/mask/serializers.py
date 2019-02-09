from rest_framework import serializers

from image.serializers import ImageSerializer
from mask.models import Mask, DefectPosition, DefectPositionImage, Defect, Ellipse


class MaskSerializer(serializers.ModelSerializer):
    create_time = serializers.ReadOnlyField()
    defect_position_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Mask
        fields = ('id', 'create_time', 'defect_position_count')

    def get_defect_position_count(self, obj):
        return DefectPosition.objects.filter(mask=obj).count()


class DefectPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectPosition
        fields = ('id', 'mask')


class EllipseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ellipse
        fields = ('id', 'centerX', 'centerY', 'x', 'y', 'rotation')


class DefectSerializer(serializers.ModelSerializer):
    ellipse = EllipseSerializer()
    class Meta:
        model = Defect
        fields = ('id', 'position_image', 'ellipse')

    def create(self, validated_data):
        ellipse = EllipseSerializer().create(validated_data['ellipse'])
        ellipse.save()
        validated_data['ellipse'] = ellipse
        return super(DefectSerializer, self).create(validated_data)


class DefectPositionImageSerializer(serializers.ModelSerializer):
    create_time = serializers.ReadOnlyField()
    image = ImageSerializer()
    defects = DefectSerializer(many=True, source='get_defects', read_only=True)

    class Meta:
        model = DefectPositionImage
        fields = ('id', 'defect_position', 'image', 'create_time', 'defects')

    def create(self, validated_data):
        image = ImageSerializer().create(validated_data['image'])
        image.save()
        validated_data['image'] = image
        return super(DefectPositionImageSerializer, self).create(validated_data)
