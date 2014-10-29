from django.shortcuts import render
from models import User
from rest_framework import viewsets
from serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LdapAuthRequest:
    def __init__(usrnm,pwd):
        self.username = usrnm
        self.password = pwd
    
class LdapAuthRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LdapAuthRequst
        fields = ('username','password')

@api_view(['POST'])
def ldap_authenticate(request):
    print user
    print pwd
    