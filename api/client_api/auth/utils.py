import random
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
import base64
import uuid
from django.core.files.base import ContentFile
import requests as r

from core.models import Account, VerificationCode


def getLoginToken(user):
    token = RefreshToken.for_user(user)
    return token


def GenerateCode():
    code = str(random.randint(100000, 999999))
    return code


def GenerateLink(user, verification_type, verification_action, email, phone_number):
    token = default_token_generator.make_token(user)
    safe_token = urlsafe_base64_encode(
        force_bytes(
            signing.dumps(
                [
                    user.pk,
                    verification_type,
                    verification_action,
                    email,
                    phone_number,
                    token,
                ]
            )
        )
    )
    if verification_action == VerificationCode.CHANGE_EMAIL:
        return f"{settings.API_ENDPOINT}/auth/account/change_email?token={safe_token}"
    elif verification_action == VerificationCode.FORGOT_PASSWORD:
        return f"{settings.WEB_LINK}?action=reset_password&token={safe_token}"


def VerifyLink(token):
    decoded_token = urlsafe_base64_decode(token)
    (
        user_pk,
        verification_type,
        verification_action,
        email,
        phone_number,
        token,
    ) = signing.loads(decoded_token.decode())
    user = Account.objects.get(pk=user_pk)

    if default_token_generator.check_token(user, token) == False:
        raise serializers.ValidationError("Bad token")

    return user, verification_type, verification_action, email, phone_number


def VerifyToken(token):
    decoded_token = urlsafe_base64_decode(token)
    (
        user_pk,
        verification_type,
        verification_action,
        email,
        phone_number,
        token,
    ) = signing.loads(decoded_token.decode())
    user = Account.objects.get(pk=user_pk)

    if default_token_generator.check_token(user, token) == False:
        raise serializers.ValidationError("Bad token")

    return user, verification_type, verification_action, email, phone_number


def get_user_wallet(user:Account):
    try:
        url = "https://account.pywe.org/v1/system/check-credit/"
        params = {'username':user.username,'password':user.password,'phone':user.phone,"email":user.email}
        raw = r.post(url=url,json=params)
    except Exception:
        return {}
    else:
        d = raw.json()
        if d.get("code") != 200:
            return d['message']
        return d['credit']
    

# def create_user_in_waiting(data:dict):
#     phone = data.get("phone")
#     user = Account()
#     user.username = phone
#     user.phone = phone
#     user.save()
#     phones = [phone]
#     # send_welcome_sms(phones,user.otp)
#     log_data = {
#     "activity_by":user,
#     "description":f"user joins :: {datetime.today()}",
#     "activity_type":"auth"
#     }
#     create_audit_trail(log_data)
#     return user



class Base64FileField(serializers.FileField):
    """
    A Django REST framework field for handling file-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.
    """
    
    def to_internal_value(self, data):
        # Check if this is a base64 string
        if isinstance(data, str) and data.startswith('data:'):
            # Decode the base64 string
            format, base64_str = data.split(';base64,')
            ext = format.split('/')[-1]  # Extract file extension (e.g., 'pdf', 'docx')
            file_data = ContentFile(base64.b64decode(base64_str), name=f"{uuid.uuid4()}.{ext}")
            return file_data
        raise serializers.ValidationError("Invalid file format")