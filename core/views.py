from django.contrib.auth import login
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView, GenericAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from .serializer import *
from django.core.cache import cache
from .validators import *
from .models import *
from rest_framework import permissions


class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user

        serializer = UserSerializer(user)
        return Response({'data': serializer.data})


# ClassView [BaseViewSet] : Root view set for all class for CRUD operation
class BaseViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, RetrieveUpdateAPIView, DestroyAPIView):

    def perform_create(self, serializer):
        """Create an object"""
        serializer.save()


class UserViewSet(BaseViewSet):
    lookupField = 'id'
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        exists = User.objects.filter(email=data['email']).exists()

        if not exists:
            response = super().create(request, *args, **kwargs)
            return response
        return Response(status=302)

    def partial_update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 201:
            normal_user = response.data
            cache.set('data_{}'.format(normal_user['id']), {
                **normal_user
            })
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = instance.id
        self.perform_destroy(instance)
        return Response(data={"id": user_id, "status": "user deleted successful"})


# ClassView [UserLogin] : To login into system
class UserLogin(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            user_obj = serializer.validated_data['user']
            new_user = UserSerializer(user_obj, context=self.get_serializer_context()).data
            login(request, user_obj)
            return Response(
                {"msg": "User Login Success !!!", "data": new_user, "token": user_obj.tokens,
                 "status_code": status.HTTP_200_OK})
        else:
            """Login Validation"""
            return userValidation(serializer.errors, "Login failed.")


# ClassView [CreateUser] : To create new user
class CreateUser(CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            new_user_data = UserSerializer(user, context=self.get_serializer_context()).data
            user_token = user.tokens
            return Response({
                "msg": "New user created successfully !!!",
                "data": new_user_data,
                "token": user_token,
                "status_code": status.HTTP_201_CREATED
            })
        else:
            """User Registration Validation"""
            return userValidation(serializer.errors, "New user registration failed.")


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "User has been logout successfully", "response_status": "Logout Success", "status_code": status.HTTP_204_NO_CONTENT})
        else:
            return Response({"msg": "Token should not be empty", "response_status": "Logout Failed",
                             "status_code": status.HTTP_406_NOT_ACCEPTABLE})
