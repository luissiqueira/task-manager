from django.contrib.auth import get_permission_codename
from guardian.admin import GuardedModelAdmin

from core.models import Role


class ObjectPermissionMixin(object):

    @staticmethod
    def can_view_obj(request, obj):
        return False

    @staticmethod
    def can_modify_obj(request, obj):
        return False

    def has_view_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('view', opts)
        if request.user.has_perm("%s.%s" % (opts.app_label, codename), obj):
            return True

        return self.can_view_obj(request, obj)

    def has_delete_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('delete', opts)
        if request.user.has_perm("%s.%s" % (opts.app_label, codename), obj):
            return True

        return self.can_modify_obj(request, obj)

    def has_change_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('change', opts)
        if request.user.has_perm("%s.%s" % (opts.app_label, codename), obj):
            return True

        return self.can_modify_obj(request, obj)

    def has_view_or_change_permission(self, request, obj=None):
        return self.has_view_permission(request, obj) or self.has_change_permission(request, obj)

    def has_add_permission(self, request, obj=None):
        opts = self.opts
        codename = get_permission_codename('add', opts)
        if request.user.has_perm("%s.%s" % (opts.app_label, codename)):
            return True

        if obj is not None:
            return self.can_modify_obj(request, obj)

        authorized_roles = (Role.ROLE_ADMIN, Role.ROLE_OPERATIONAL)
        return request.user.roles.filter(role__in=authorized_roles).exists()


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


class BaseModelAdmin(ObjectPermissionMixin, SaveCreatorMixin, GuardedModelAdmin):
    pass
