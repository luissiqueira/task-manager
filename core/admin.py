from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline

from .models import Project, Task, Organization, ObjectRole, ObjectAttachment, TaskNote


class ObjectRoleInlineAdmin(GenericStackedInline):
    model = ObjectRole
    extra = 0
    fields = ('user', 'role',)


class ObjectAttachmentInlineAdmin(GenericStackedInline):
    model = ObjectAttachment
    extra = 0
    fields = ('attachment',)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    readonly_fields = ('deleted',)
    inlines = [ObjectRoleInlineAdmin, ObjectAttachmentInlineAdmin]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.id and hasattr(obj, 'creator'):
                obj.creator = request.user
        formset.save()


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'organization')
    list_filter = ('status', 'organization')
    search_fields = ('title', 'description', 'organization__name')
    readonly_fields = ('deleted',)
    inlines = [ObjectRoleInlineAdmin, ObjectAttachmentInlineAdmin]


class TaskNoteInlineAdmin(admin.StackedInline):
    model = TaskNote
    extra = 0
    exclude = ('deleted', 'creator')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('deleted',)
    inlines = [ObjectAttachmentInlineAdmin, TaskNoteInlineAdmin]
