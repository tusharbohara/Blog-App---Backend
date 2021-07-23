from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create', UserViewSet)
router.register('login', UserLogin)
router.register('userView', AuthUserAPIView)

urlpatterns = [
    path('', include(router.urls))
]
