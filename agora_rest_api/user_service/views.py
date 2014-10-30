from django.shortcuts import render
from models import User
from rest_framework import viewsets
from rest_framework import status
from serializers import UserSerializer
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ldapViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
        