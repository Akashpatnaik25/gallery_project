from rest_framework import serializers
from .models import UploadedImage


class GallerySerilaizers(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = "__all__"

    