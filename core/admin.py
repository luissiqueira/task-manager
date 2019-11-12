from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.admin import GenericStackedInline
from guardian.admin import GuardedModelAdmin

from .models import Project, Task, Organization, ObjectRole, ObjectAttachment, TaskNote


class ObjectPermissionMixin(object):
    def has_view_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('view', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename), obj)

    def has_delete_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('delete', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename), obj)

    def has_change_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('change', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename), obj)

    def has_view_or_change_permission(self, request, obj=None):
        return self.has_view_permission(request, obj) or self.has_change_permission(request, obj)

    def has_add_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('add', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))


class ObjectRoleInlineAdmin(ObjectPermissionMixin, GenericStackedInline):
    model = ObjectRole
    extra = 0
    fields = ('user', 'role',)


class ObjectAttachmentInlineAdmin(GenericStackedInline):
    model = ObjectAttachment
    extra = 0
    fields = ('attachment',)


class SaveCreatorMixin(object):
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.id and hasattr(obj, 'creator'):
                obj.creator = request.user
        formset.save()

    def save_model(self, request, obj, form, change):
        if not obj.creator:
            obj.creator = request.user
        return super(SaveCreatorMixin, self).save_model(request, obj, form, change)


@admin.register(Organization)
class OrganizationAdmin(ObjectPermissionMixin, SaveCreatorMixin, GuardedModelAdmin):
    readonly_fields = ('deleted',)

    inlines = [ObjectRoleInlineAdmin, ObjectAttachmentInlineAdmin]


@admin.register(Project)
class ProjectAdmin(ObjectPermissionMixin, SaveCreatorMixin, GuardedModelAdmin):
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
class TaskAdmin(GuardedModelAdmin):
    list_display = ('id', 'title', 'priority', 'status', 'agreed_date', 'final_date', 'project')
    list_filter = ('priority', 'status', 'agreed_date', 'project', 'project__organization')
    readonly_fields = ('deleted',)
    inlines = [ObjectAttachmentInlineAdmin, TaskNoteInlineAdmin]
