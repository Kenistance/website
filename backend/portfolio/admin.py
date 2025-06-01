from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_at',
        'requires_payment',
        'price',
        'has_file',
        'has_download_link',
    )
    list_filter = ('requires_payment', 'created_at')
    search_fields = ('title', 'description')

    def has_file(self, obj):
        return bool(obj.file_path)
    has_file.boolean = True
    has_file.short_description = 'Internal File'

    def has_download_link(self, obj):
        return bool(obj.download_url)
    has_download_link.boolean = True
    has_download_link.short_description = 'Download URL'
