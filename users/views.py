from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from .serializers import SignUpSerializer
from .models import  User



class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny,]
