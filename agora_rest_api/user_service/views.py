from django.shortcuts import render
from models import User
from rest_framework import viewsets
from rest_framework import status
from serializers import UserSerializer
<<<<<<< HEAD
from django.http import HttpResponse, HttpResponseNotFound
=======
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.http import HttpResponse
>>>>>>> 2824223e4db6ffe319926745aa09fcf78a393187

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
<<<<<<< HEAD
    
class ldapViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
        
=======

class LdapAuthRequest:
    def __init__(usrnm,pwd):
        self.username = usrnm
        self.password = pwd
    
class LdapAuthRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LdapAuthRequest
        fields = ('username','password')

@api_view(['GET'])
def ldap_authenticate(request):
    return HttpResponse(status=200)
    
>>>>>>> 2824223e4db6ffe319926745aa09fcf78a393187
