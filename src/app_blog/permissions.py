from rest_framework.permissions import BasePermission


class BaseGroupPermission(BasePermission):
    """
    Base permission for checking user groups.
    Child classes should override allowed_groups.
    """

    allowed_groups = []

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # The Django administrator always has access.
        if request.user.is_superuser:
            return True

        return request.user.groups.filter(name__in=self.allowed_groups).exists()


class IsViewerOrHigher(BaseGroupPermission):
    """
    Viewer, Editor or Admin.
    """

    allowed_groups = [
        "Viewer",
        "Editor",
        "Admin",
    ]


class IsEditorOrAdmin(BaseGroupPermission):
    """
    Editor or Admin.
    """

    allowed_groups = [
        "Editor",
        "Admin",
    ]


class IsOwnerOrAdmin(BasePermission):
    """
    Object owner or Admin group member.
    """

    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser:
            return True

        if request.user.groups.filter(name="Admin").exists():
            return True

        return obj.author == request.user
