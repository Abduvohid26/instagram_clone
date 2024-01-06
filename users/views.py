from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import SignUpSerializer, UserSerializer
from .models import  User



class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny,]
