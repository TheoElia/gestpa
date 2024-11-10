import random
import re
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.utils import dateformat, timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

from core.models import Account


class AllowAllPermission(BasePermission):
    """
    A custom permission class that allows unrestricted access.
    """

    def has_permission(self, request, view):
        return True


def getLoginToken(member):
    token = RefreshToken.for_user(member)
    return token


def get_object_or_404_with_error(error, model, **kwargs):
    instances = model.objects.filter(**kwargs)
    count = len(instances)
    if count == 0:
        raise serializers.ValidationError(error)
    elif count > 1:
        raise serializers.ValidationError(f"Non unique: {error}")
    elif count == 1:
        return instances[0]


def CheckPasswordValidity(password):
    if len(password) < 8:
        return False

    if not re.compile(r".*\d+.*").match(password):
        return False

    if not re.compile(r".*[a-z]+.*").match(password):
        return False

    if not re.compile(r".*[A-Z]+.*").match(password):
        return False

    return True


def generate_token(length):
    return "".join([random.choice("1234567890") for _ in range(length)])


def generate_transaction_id(processor_transaction):
    now = dateformat.format(timezone.now(), "Y-m-d-H:i:s")
    transaction = processor_transaction.transaction
    return f"{now}-{transaction.client.pk}"


def generate_secret(account, event):
    token = default_token_generator.make_token(account)
    safe_token = urlsafe_base64_encode(
        force_bytes(signing.dumps([account.id, event.id, token]))
    )
    return safe_token


def verify_secret(token):
    decoded_token = urlsafe_base64_decode(token)
    account_id, event_id, token = signing.loads(decoded_token.decode())
    account = Account.objects.get(pk=account_id)

    if not default_token_generator.check_token(account, token):
        raise serializers.ValidationError("Wrong token")

    return account, event_id

def generate_password():
    return "@hello222"


def generate_unique_id(length:int):
    # Generate a UUID and take the integer representation
    unique_id = uuid.uuid4().int
    # Convert the integer to a string and slice it to get the first 15 digits
    return str(unique_id)[:length]