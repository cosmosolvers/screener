from cash.models import User
from cash.serializers import (
    SignSerializer,
    FringerSignSerializer,
    UserSerializer
)
from rest_framework import permissions, status, viewsets


class SignUpSerializer(viewsets.ModelViewSet):
    pass


class SignInSerializer(viewsets.ModelViewSet):
    pass


class FringerSignSerializer(viewsets.ModelViewSet):
    pass


class UserSerializer(viewsets.ModelViewSet):
    pass
