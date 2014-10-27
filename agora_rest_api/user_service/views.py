from django.shortcuts import render
from models import User
from rest_framework import viewsets
from serializers import UserSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer