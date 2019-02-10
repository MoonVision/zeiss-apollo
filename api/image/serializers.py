from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PILImage
from rest_framework import serializers


from image.models import Image


class ImageSerializer(serializers.ModelSerializer):
    create_time = serializers.ReadOnlyField()
    width = serializers.IntegerField(read_only=True)
    height = serializers.IntegerField(read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'create_time', 'image', 'width', 'height')

    def create(self, validated_data):
        if validated_data['image'].name.endswith('.tif') or validated_data['image'].name.endswith('.tiff'):
            image = PILImage.open(validated_data['image'])
            out = image.convert("RGB")
            bytes = BytesIO()
            out.save(bytes, format="jpeg")
            validated_data['image'] = InMemoryUploadedFile(bytes, None, 'test.jpeg', 'image/jpeg', None, None)

        return super(ImageSerializer, self).create(validated_data)
