from rest_framework import serializers

from image.serializers import ImageSerializer
from mask.models import Mask, DefectPosition, DefectPositionImage, Defect, Ellipse


class MaskSerializer(serializers.ModelSerializer):
    create_time = serializers.ReadOnlyField()
    defect_position_count = serializers.SerializerMethodField(read_only=True)
    defect_image_count = serializers.SerializerMethodField(read_only=True)
    defect_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Mask
        fields = ('id', 'create_time', 'defect_position_count', 'defect_image_count', 'defect_count')

    def get_defect_position_count(self, obj):
        return DefectPosition.objects.filter(mask=obj).count()

    def get_defect_image_count(self, obj):
        return DefectPositionImage.objects.filter(defect_position__mask=obj).count()

    def get_defect_count(self, obj):
        return Defect.objects.filter(position_image__defect_position__mask=obj).count()


class DefectPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefectPosition
        fields = ('id', 'mask', 'x', 'y')


class EllipseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ellipse
        fields = ('id', 'centerX', 'centerY', 'x', 'y', 'rotation')


class DefectSerializer(serializers.ModelSerializer):
    ellipse = EllipseSerializer()
    class Meta:
        model = Defect
        fields = ('id', 'position_image', 'ellipse')

    def __init__(self, *args, remove_position_image=False, **kwargs):
        super(DefectSerializer, self).__init__(*args, **kwargs)
        if remove_position_image:
            self.fields.pop('position_image')

    def create(self, validated_data):
        ellipse = EllipseSerializer().create(validated_data['ellipse'])
        ellipse.save()
        validated_data['ellipse'] = ellipse
        return super(DefectSerializer, self).create(validated_data)


class DefectPositionImageSerializer(serializers.ModelSerializer):
    mask_id = serializers.IntegerField(write_only=True)
    position_x = serializers.IntegerField(write_only=True)
    position_y = serializers.IntegerField(write_only=True)
    create_time = serializers.ReadOnlyField()
    defect_position = serializers.PrimaryKeyRelatedField(queryset=DefectPosition.objects.all(), required=False)
    image = serializers.ImageField()
    defects = DefectSerializer(many=True, source='get_defects', read_only=True)
    new_defects = DefectSerializer(many=True, remove_position_image=True, write_only=True)

    class Meta:
        model = DefectPositionImage
        fields = ('id', 'defect_position', 'image', 'create_time', 'mask_id', 'defects', 'position_x', 'position_y', 'new_defects')

    def create(self, validated_data):
        image = ImageSerializer().create({'image':validated_data['image']})
        image.save()
        validated_data['image'] = image
        print(validated_data)
        defects = validated_data.pop('new_defects')
        defection_position_image = super(DefectPositionImageSerializer, self).create(validated_data)
        for d in defects:
            d['position_image'] = defection_position_image
        DefectSerializer(many=True).create(defects)
        return defection_position_image
