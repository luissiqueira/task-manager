from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.db.models import Q

from core.mixins import ObjectPermissionMixin, BaseModelAdmin
from .models import Project, Task, Organization, ObjectRole, ObjectAttachment, TaskNote, Role


class ObjectRoleInlineAdmin(ObjectPermissionMixin, GenericStackedInline):
    model = ObjectRole
    extra = 0
    fields = ('user', 'role',)
    exclude = ('deleted', 'creator')


class ObjectAttachmentInlineAdmin(GenericTabularInline):
    model = ObjectAttachment
    extra = 0
    fields = ('attachment', 'creator',)
    readonly_fields = ('creator',)
    exclude = ('deleted',)

    def has_add_permission(self, request, obj=None):
        if isinstance(obj, Project):
            return ProjectAdmin.can_modify_obj(request, obj)

        opts = self.opts
        codename = get_permission_codename('add', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))


@admin.register(Organization)
class OrganizationAdmin(BaseModelAdmin):
    exclude = ('deleted', 'creator')

    inlines = [ObjectRoleInlineAdmin, ObjectAttachmentInlineAdmin]

    def has_add_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('add', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(roles__user=request.user, roles__role=Role.ROLE_ADMIN).distinct()

    @staticmethod
    def can_view_obj(request, obj):
        return request.user.roles.filter(role=Role.ROLE_ADMIN, content_type__model='organization').exists()


@admin.register(Project)
class ProjectAdmin(BaseModelAdmin):
    list_display = ('title', 'status', 'organization')
    list_filter = ('status', 'organization')
    search_fields = ('title', 'description', 'organization__name')
    readonly_fields = ('deleted',)
    exclude = ('deleted', 'creator')
    inlines = [ObjectRoleInlineAdmin, ObjectAttachmentInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(Q(roles__user=request.user) | Q(organization__roles__user=request.user)).distinct()

    @staticmethod
    def can_view_obj(request, obj):
        if obj is not None:
            if obj.roles.filter(user=request.user).exists():
                return True
            if obj.organization and obj.organization.roles.filter(user=request.user).exists():
                return True
        return super(ProjectAdmin, ProjectAdmin).can_view_obj(request, obj)

    @staticmethod
    def can_modify_obj(request, obj):
        if obj is not None:
            authorized_roles = (Role.ROLE_ADMIN, Role.ROLE_OPERATIONAL)
            filters = {'user': request.user, 'role__in': authorized_roles}

            if obj.roles.filter(**filters).exists():
                return True
            if obj.organization and obj.organization.roles.filter(**filters).exists():
                return True
        return super(ProjectAdmin, ProjectAdmin).can_modify_obj(request, obj)


class TaskNoteInlineAdmin(admin.StackedInline):
    model = TaskNote
    extra = 0
    readonly_fields = ('creator',)
    exclude = ('deleted',)


@admin.register(Task)
class TaskAdmin(BaseModelAdmin):
    list_display = ('title', 'responsible', 'priority', 'status', 'agreed_date', 'final_date', 'project')
    list_filter = ('priority', 'status', 'responsible', 'agreed_date', 'project', 'project__organization')
    readonly_fields = ('deleted',)
    search_fields = ('title', 'description')
    exclude = ('deleted', 'creator')
    inlines = [ObjectAttachmentInlineAdmin, TaskNoteInlineAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(
            Q(responsible=request.user) |
            Q(project__roles__user=request.user) |
            Q(project__organization__roles__user=request.user)
        ).distinct()

    @staticmethod
    def can_view_obj(request, obj):
        if obj:
            if obj.responsible == request.user:
                return True
            if obj.project:
                project = obj.project
                if project.roles.filter(user=request.user).exists():
                    return True
                if project.organization and project.organization.roles.filter(user=request.user).exists():
                    return True

        return super(TaskAdmin, TaskAdmin).can_view_obj(request, obj)

    @staticmethod
    def can_modify_obj(request, obj):
        if obj:
            if obj.responsible == request.user:
                return True
            if obj.project:
                project = obj.project
                authorized_roles = (Role.ROLE_ADMIN, Role.ROLE_OPERATIONAL)
                filters = {'user': request.user, 'role__in': authorized_roles}

                if project.roles.filter(**filters).exists():
                    return True
                if project.organization and project.organization.roles.filter(**filters).exists():
                    return True
        return super(TaskAdmin, TaskAdmin).can_modify_obj(request, obj)
