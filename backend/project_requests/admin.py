from django.contrib import admin
from .models import ProjectRequest

@admin.register(ProjectRequest)
class ProjectRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ('status',)
    search_fields = ('title',)
