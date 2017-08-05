from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSelfOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.pk != obj.pk:
            return request.method in SAFE_METHODS
        return True
