# backend/portfolio/admin.py

from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'project_type',
        'price',
        'has_download_url',  # Add custom methods for boolean display
        'has_file_path',     # Add custom methods for boolean display
        'has_website_url',   # Add custom methods for boolean display
        'demo_url',
        'created_at',
    )
    list_filter = ('project_type', 'price', 'created_at')
    search_fields = ('title', 'description', 'website_url', 'download_url')

    # Custom methods to display boolean flags in the admin list view
    def has_download_url(self, obj):
        return bool(obj.download_url)
    has_download_url.boolean = True
    has_download_url.short_description = 'Download URL'

    def has_file_path(self, obj):
        return bool(obj.file_path)
    has_file_path.boolean = True
    has_file_path.short_description = 'Internal File'

    def has_website_url(self, obj):
        return bool(obj.website_url)
    has_website_url.boolean = True
    has_website_url.short_description = 'Website URL'

    # Define fieldsets to organize fields in the add/change form
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image_url', 'demo_url')
        }),
        ('Project Type & Links', {
            'fields': ('project_type', 'website_url', 'download_url', 'file_path', 'price'),
            'description': "Define if this is a downloadable program or a linked website, and its associated files/links and price."
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',), # Makes this section collapsible
        }),
    )
    readonly_fields = ('created_at',) # Ensure created_at is not editable