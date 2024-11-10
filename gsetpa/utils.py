import datetime
import jwt
from django.conf import settings
from rest_framework import pagination,serializers
from rest_framework.response import Response

def authenticate_pub(secret_name):
    if secret_name:
        # TODO(): check if pub 'public_key' authentic from AWS Secrets Manager
        pass
    return True


def generate_access_token(secret_name):
    if authenticate_pub(secret_name):
        access_token_payload = {
            'secret_name': secret_name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
            'iat': datetime.datetime.utcnow(),
        }
        access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256')
    else:
        access_token = None
    return access_token


def validate_token(access_token):
    payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
    secret_name = payload.get('secret_name')
    return authenticate_pub(secret_name)


def get_object_or_404_with_error(error, model, **kwargs):
    instances = model.objects.filter(**kwargs)
    count = len(instances)
    if count == 0:
        raise serializers.ValidationError(error)
    elif count > 1:
        raise serializers.ValidationError(f"Non unique: {error}")
    elif count == 1:
        return instances[0]


class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "total_count": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "count": len(data),
                "data": data,
            }
        )
