from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'start_date',
                    'deadline', 'created_at')
    list_filter = ('organization',)
    search_fields = ('name',)
