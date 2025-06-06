# backend/portfolio/serializers.py
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    # Removed get_download_link as frontend will handle logic directly
    # and use website_url or download_url based on project_type and price.

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'image_url',       # Keep this, your frontend uses 'image' which image_url can map to
            'created_at',
            # 'requires_payment', # Removed, as price > 0 implies payment
            'price',
            'demo_url',
            # 'download_link',    # Removed, as frontend directly uses download_url or website_url
            'download_url',    # Expose the direct download URL
            # New fields
            'project_type',
            'website_url',
        ]