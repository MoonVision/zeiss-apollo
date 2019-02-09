from rest_framework import serializers

from image.models import Image


class ImageSerializer(serializers.ModelSerializer):
    create_time = serializers.ReadOnlyField()
    width = serializers.IntegerField(read_only=True)
    height = serializers.IntegerField(read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'create_time', 'image', 'width', 'height')

