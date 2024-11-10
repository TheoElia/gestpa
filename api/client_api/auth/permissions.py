from rest_framework.permissions import IsAuthenticated

from core.models import Account


class LoginPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.account_type == Account.MEMBER
        return False


class SetMFAPermission(IsAuthenticated):
    pass


class ProfilePermission(IsAuthenticated):
    def has_object_permission(self, request, view, object, *args, **kwargs):
        return request.user.id == object.id
