from django.contrib import admin
from .models import Project, Task


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'description')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
