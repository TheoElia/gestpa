from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken
from rest_framework_simplejwt.settings import api_settings

from core.models import Account, AdminUser


class GSETBackendAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = AdminUser.objects.get(username=username)
            if user.check_password(password):
                return user
            else:
                return None
        except AdminUser.DoesNotExist:
            if username and username == settings.ADMIN_USERNAME:
                user = AdminUser.objects.create(
                    username=username, is_superuser=True, is_staff=True
                )
                user.set_password(password)
                user.save()
                return user
            return None

    def get_user(self, user_id):
        try:
            return AdminUser.objects.get(pk=user_id)
        except AdminUser.DoesNotExist:
            return None


class GSETMemberAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = Account

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            member_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))
        try:
            user = Account.objects.only("id").get(
                **{api_settings.USER_ID_FIELD: member_id}
            )
        except Account.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")
        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
        return user
