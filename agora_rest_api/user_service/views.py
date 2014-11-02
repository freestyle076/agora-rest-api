from django.shortcuts import render
from models import User
from rest_framework import viewsets
from rest_framework import status
from serializers import UserSerializer
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers
from django.http import HttpResponse
import ldap
import json

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ldapViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LdapAuthRequest:
    def __init__(usrnm,pwd):
        self.username = usrnm
        self.password = pwd
    
class LdapAuthRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LdapAuthRequest
        fields = ('username','password')

@api_view(['POST'])
def ldap_authenticate(request):
    json_data = {}
    try:
        #attempt connection to ldap server
        handle = ldap.open('dc-ad-gonzaga.gonzaga.edu')
        try:
            #attempt bind with username and password gonzaga.edu
            handle.simple_bind_s('khandy@gonzaga.edu', 'wrong')
            #if successful return OK, username+pwd is in the ldap database!
            json_data['email'] = 'khandy@gonzaga.edu'
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
            return response
            
        except ldap.LDAPError, error_message:
            try:
                #attempt bind with username and password gonzaga.edu
                handle.simple_bind_s('khandy@zagmail.gonzaga.edu','wrong')
                #if successful return OK, username+pwd is in the ldap database!
                json_data['email'] = 'khandy@gonzaga.edu'
                response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
                return response
                
            except ldap.LDAPError, error_message:
                #username+password not in ldap database, return bad request
                response = HttpResponse(status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
                return response
                
    except ldap.LDAPError, error_message:
        #failure to connect to ldap server
        response = HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type='application/json')
        response.write(error_message)
        return response
        
    
