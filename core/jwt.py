from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header, BaseAuthentication
from django.conf import settings
import jwt
from .models import User


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        auth_header = get_authorization_header(request)
        auth_data = auth_header.decode('utf-8')
        auth_token = auth_data.split(" ")
        if len(auth_token) != 2:
            raise exceptions.AuthenticationFailed('Token is not valid')
        token = auth_token[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            email = payload['email']
            user = User.objects.get(email=email)
            return user, token
        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('Token is expired, Login again')
        except jwt.DecodeError as ex:
            raise exceptions.AuthenticationFailed('Token is invalid')
        except User.DoesNotExist as no_user:
            raise exceptions.AuthenticationFailed('No such user')
        return super().authenticate(request)
