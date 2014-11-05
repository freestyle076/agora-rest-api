from models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from serializers import UserSerializer
from django.http import HttpResponse
from django.db import utils
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
import ldap
import json
import ast
import sys

'''
Views for the user_service API application. The following views expose user
API methods for authenticating a user login, creating a user and editing a user
account.
'''


class UserViewSet(viewsets.ModelViewSet):
    '''
    Django standard ViewSet for User objects.
    route: /users/
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def create_user(request):
    '''
    POST method for creating a user. Request body must contain the following
    data in JSON format:
        username: username of the new user
        first_name: First name of user
        last_name: Last name of user
        gonzaga_email: LDAP authenticated Gonzaga provided user email
        pref_email: User provided preferred email*
        phone: User provided phone number*
    *-Nullable values
    route: /createuser/
    '''
    
    #parse request body for user information
    new_user_info = ast.literal_eval(request.body)    
    #validate the preferred email field if provided
    if new_user_info['pref_email'] not in ["",None]:
        pref_email = new_user_info['pref_email']
        #ensure the preferred email isn't a zagmail.gonzaga.edu or gonzaga.edu domain
        if '@zagmail.gonzaga.edu' in pref_email or '@gonzaga.edu' in pref_email:
            #return bad_request 400 code
            response = HttpResponse(status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            response.write("ERROR: The submitted user preferred email is suffixed with a Gonzaga domain.")
            return response
    
    #try to create and save the user
    try:
        created_user = User.objects.create(
            username=new_user_info['username'],
            first_name=new_user_info['first_name'],
            last_name=new_user_info['last_name'],
            gonzaga_email=new_user_info['gonzaga_email'],
            pref_email=new_user_info['pref_email'],
            phone=new_user_info['phone'])
        created_user.save()
        
        #if no exception thrown return success
        return HttpResponse(status=status.HTTP_200_OK)
        
    #IntegrityError indicates create user failed from 
    #bad foreign key or duplicate primary key, in this case
    #gonzaga_email or username
    except utils.IntegrityError as e:
        response = HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        response.write(str(e))
        return response
    except:
        e = sys.exc_info()[0]
        response = HttpResponse(status=status.HTTP_400_BAD_REQUEST)
        response.write(e)
        return response

@api_view(['POST'])
def view_user(request):
    '''
    GET method for retrieving User data to be viewed. 
    Request body must contain the following data in JSON format:
        username: username of the user to authenticate
    route: /userprofile/
    '''
    json_data = {}
    #parse request body for incoming login data
    info = ast.literal_eval(request.body)
    user = info['username']
    json_data['firstname'] = User.objects.get(username=user).first_name
    json_data['lastname'] = User.objects.get(username=user).last_name
    response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    return response
    
@api_view(['POST'])
def ldap_authenticate(request):
    '''
    POST method for authenticating a user login. Request body must contain the 
    following data in JSON format:
        username: username of the user to authenticate
        password: entered password to authenticate
    route: /ldapauth/
    '''
    #parse request body for incoming login data
    info = ast.literal_eval(request.body)
    user = info['username']
    info['username'] = info['username'] + '@zagmail.gonzaga.edu'
    json_data = {}
    
    #check for empty password; LDAP passes requests with empty passwords, we don't
    if(info['password'] == ""):
        json_data['message'] = 'Empty Password'
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
    
    #attempt connection to ldap server
    try:
        handle = ldap.open('dc-ad-gonzaga.gonzaga.edu')
        
        #attempt bind on user provided credentials with email @zagmail.gonzaga.edu
        try:
            handle.simple_bind_s(info['username'], info['password'])
            
            #if successful return OK, username+pwd is in the ldap database!
            json_data['message'] = 'Authentication succesful!'
            #checks if user is already in our database, assigns variable yes if so
            if User.objects.filter(username=user).exists():
                json_data['exists'] ='yes'
            else:
                json_data['exists'] ='no'
            json_data['email'] = info['username']
            info = None #clear traces of user information after done using
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
            return response
        #catch exception, the zagmail suffix didn't work
        except ldap.LDAPError, error_message:
            #attempt bind on user provided credentials with email @gonzaga.edu
            try:
                #replace email suffix
                info['username'] = info['username'].replace('@zagmail.gonzaga.edu','@gonzaga.edu')
                
                #attempt bind with username and password gonzaga.edu
                handle.simple_bind_s(info['username'],info['password'])
                
                #if successful return OK, username+pwd is in the ldap database!
                json_data['message'] = 'Authentication succesful!'
                
                #checks if user is already in our database, assigns variable yes if so
                if User.objects.filter(username=user).exists():
                    json_data['exists'] ='yes'
                else:
                    json_data['exists'] ='no'
                    
                json_data['email'] = info['username']
                response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
                info = None #clear traces of user information after done using
                return response
            
            #catch exception, neither username+email_suffix+password in ldap database, return bad request
            except ldap.LDAPError, error_message:
                json_data['message'] = 'Invalid Credentials'
                response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
                return response
                
    #failure to connect to ldap server, return internal server error   
    except ldap.LDAPError, error_message:
        json_data['message'] = 'Error Connecting to Ldap Server'
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type='application/json')
        response.write(error_message)
        return response
        
    
