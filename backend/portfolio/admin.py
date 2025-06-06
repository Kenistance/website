# backend/portfolio/admin.py

from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'project_type',     # New field
        'price',
        'website_url',      # New field
        'download_url',
        'demo_url',
        'created_at',
        # 'has_file', # Removed, as file_path existence implies it
        # 'has_download_link', # Removed, as download_url existence implies it
    )
    list_filter = ('project_type', 'price', 'created_at') # Filter by new fields
    search_fields = ('title', 'description', 'website_url', 'download_url')

    