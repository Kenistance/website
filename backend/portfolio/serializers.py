from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    download_link = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'image_url',
            'created_at',
            'requires_payment',
            'price',
            'demo_url',
            'download_link',  # dynamic field
        ]

    def get_download_link(self, obj):
        if not obj.requires_payment:
            return obj.download_url
        return None  # or return a message like "Payment required"
