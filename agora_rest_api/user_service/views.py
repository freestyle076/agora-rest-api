from django.shortcuts import render
from models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from serializers import UserSerializer
from django.http import HttpResponse, HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import ldap
import ast

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ldapViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
'''
class LdapAuthRequest:
    def __init__(usrnm,pwd):
        self.username = usrnm
        self.password = pwd
    
class LdapAuthRequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LdapAuthRequest
        fields = ('username','password')
'''
@api_view(['POST'])
def ldap_authenticate(request):
    info = ast.literal_eval(request.body)
    info['username'] = info['username'] + '@zagmail.gonzaga.edu'
    try:
        #attempt connection to ldap server
        handle = ldap.open('dc-ad-gonzaga.gonzaga.edu')
        try:
            #attempt bind with username and password gonzaga.edu
            handle.simple_bind_s(info['username'], 'wrong')
            #if successful return OK, username+pwd is in the ldap database!
            return HttpResponse(status=status.HTTP_200_OK)
            
        except ldap.LDAPError, error_message:
            try:
                info['username'] = info['username'].replace('@zagmail.gonzaga.edu','@gonzaga.edu')
                #attempt bind with username and password gonzaga.edu
                handle.simple_bind_s(info['username'],info['password'])
                #if successful return OK, username+pwd is in the ldap database!
                return HttpResponse(status=status.HTTP_200_OK)
                
            except ldap.LDAPError, error_message:
                #username+password not in ldap database, return bad request
                response = HttpResponse(status=status.HTTP_400_BAD_REQUEST)
                response.write(error_message)
                return response
                
    except ldap.LDAPError, error_message:
        #failure to connect to ldap server
        response = HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response.write(error_message)
        return response
        
    
