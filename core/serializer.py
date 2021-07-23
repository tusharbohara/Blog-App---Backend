from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers, exceptions, status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User


# Serializer [UserSerializer] : User data
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'
        read_only_fields = ['id', 'token']
        extra_kwargs = {'password': {'min_length': 8}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


# Serializer [LoginSerializer] : Serializer to login into system
class LoginSerializer(serializers.Serializer):
    '''required field for login'''
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        '''check email and password contains data'''
        if email and password:
            '''if email and password contains data'''
            '''Check user is authenticated or not'''
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            if user:
                '''If user is authenticated'''
                if user.is_active and not user.is_deActive:
                    '''If logged in user is active and profile is not deactivated'''
                    attrs['user'] = user
                else:
                    '''If logged in user is active but profile is deactivated'''
                    raise exceptions.ValidationError('Your account has been temporarily deactivated.')
            else:
                '''If user is not authenticated'''
                raise exceptions.ValidationError('Unable to login with given credentials')
        else:
            '''if email and password does not contains any value'''
            raise exceptions.ValidationError('Email and Password should not be empty')
        return super().validate(attrs)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            raise exceptions.ValidationError({"msg": "Invalid Token", "response_status": "Logout Failed",
                                              "status_code": status.HTTP_406_NOT_ACCEPTABLE})
