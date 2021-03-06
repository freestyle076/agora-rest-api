
from rest_framework import status
from rest_framework.decorators import api_view

from django.http import HttpResponse
from django.db import utils
from django.core import validators

from models import User, Analytics
from agora_rest_api.post_service import post_list_views
from agora_rest_api import settings

import ldap
import json
import ast
import sys
import pytz

'''
Views for the user_service API application. The following views expose user
API methods for authenticating a user login, creating a user and editing a user
account.
'''

time_zone_loc = pytz.timezone(settings.TIME_ZONE)
time_zone_utc = pytz.timezone('UTC')

@api_view(['POST'])
def edit_user(request):
    '''
    PUT method for creating a user. Request body must contain the following
    data in JSON format:
        username: username of the existing user
        first_name: New first name of user
        last_name: New Llast name of user
        pref_email: New user provided preferred email*
        phone: New user provided phone number*
    *-Nullable values
    route: /edituser/
    '''
    json_data = {}

    #attempting edit on provided json data
    try:
        request_data = ast.literal_eval(request.body) #parse data
        
        #changes to pref_email must be validatad as email (pass empty string)
        pref_email = request_data['pref_email']
        if(pref_email != ""):
            #make sure that the preferred email isn't a gonzaga email
            if '@zagmail.gonzaga.edu' in pref_email or '@gonzaga.edu' in pref_email:
                #return bad_request 400 code if preferred email is gonzaga email
                json_data['message'] = "Invalid email"
                response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
                request_data = None #clear traces of user information after done using
                return response
            try:
                #use django email validator to validate eamil address
                validators.validate_email(request_data['pref_email'])
            except validators.ValidationError:
                json_data['message'] = "Enter a valid email address."
                response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
                request_data = None #clear traces of user information after done using
                return response     

        #make edits
        edit_user = User.objects.get(username=request_data['username'])
        edit_user.first_name = request_data['first_name']
        edit_user.last_name = request_data['last_name']
        edit_user.pref_email = request_data['pref_email']
        edit_user.phone = request_data['phone']
        edit_user.save() #save edits
        
        #respond with success and HTTP 200 OK 
        json_data['message'] = "Successfully edited user " + request_data['username']
        request_data = None #clear traces of user information after done using
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    except:
        #error occured in parsing data or assigning edits
        json_data['message'] = sys.exc_info()[0]
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response

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
    
    #json dictionary
    json_data = {}    
    
    #parse request body for user information
    request_data = ast.literal_eval(request.body)
    
    #validate gonzaga email using email validator 
    try:
        validators.validate_email(request_data['gonzaga_email'])
    except validators.ValidationError as e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response    
    
    #validate the preferred email field if provided
    if request_data['pref_email']:
        pref_email = request_data['pref_email']
        #ensure the preferred email isn't a zagmail.gonzaga.edu or gonzaga.edu domain
        if '@zagmail.gonzaga.edu' in pref_email or '@gonzaga.edu' in pref_email:
            #return bad_request 400 code
            json_data['message'] = "The submitted user preferred email is suffixed with a Gonzaga domain."
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            return response
        #while we are here we will validate the preferred email as an email address
        try:
            validators.validate_email(request_data['pref_email'])
        except validators.ValidationError as e:
            print str(e)
            json_data['message'] = "Enter a valid email address."
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            request_data = None #clear traces of user information after done using
            return response
    #try to create and save the user
    try:
        created_user = User.objects.create(
            username=request_data['username'],
            first_name=request_data['first_name'],
            last_name=request_data['last_name'],
            gonzaga_email=request_data['gonzaga_email'],
            pref_email=request_data['pref_email'],
            phone=request_data['phone'])
        created_user.save()
        #Increment number of Users
        analytic = Analytics.objects.get(id=1)
        analytic.num_users = analytic.num_users + 1 
        analytic.save()
        #if no exception thrown return success
        json_data['message'] = "Successfully created user!"
        request_data = None #clear traces of user information after done using
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        
    #IntegrityError indicates create user failed from 
    #bad foreign key or duplicate primary key, in this case
    #gonzaga_email or username
    except utils.IntegrityError as e:
        print str(e)
        json_data['message'] = str(e) + " - broken uniqueness or foreign key constraint in create"
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response
    #general exception catching
    except Exception, e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response

@api_view(['POST'])
def view_user(request):
    '''
    POST method for retrieving User data to be viewed. 
    Request body must contain the following data in JSON format:
        username: username of the user to authenticate
    route: /userprofile/
    '''
    try:
        #parse request body for incoming login data
        request_data = ast.literal_eval(request.body)
        user = request_data['username']
        json_data = {}
        json_data['firstname'] = User.objects.get(username=user).first_name
        json_data['lastname'] = User.objects.get(username=user).last_name
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response
    
    except Exception, e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        request_data = None #clear traces of user information after done using
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
    request_data = ast.literal_eval(request.body)
    json_data = {}
    
    #get user entered credentials
    user = request_data['username']
    password = request_data['password']

    #allow admin to enter application without LDAP Auth   
    if user == settings.APPLE_USERNAME and password == settings.APPLE_PASS:
        #if successful return OK, username+pwd is in the ldap database!
        json_data['message'] = 'Authentication succesful!'
        #checks if user is already in our database, assigns variable yes if so
        if User.objects.filter(username=user).exists():
            json_data['exists'] ='yes'
            json_data['first_name'] = User.objects.get(username=user).first_name
            json_data['last_name'] = User.objects.get(username=user).last_name
            json_data['p_email'] = User.objects.get(username=user).pref_email
            json_data['phone'] = User.objects.get(username=user).phone 
        else:
            json_data['exists'] ='no'
        json_data['username'] = user
        json_data['g_email'] = 'adm!n@zagmail.gonzaga.edu'
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response
        
    request_data['username'] = request_data['username'] + '@zagmail.gonzaga.edu'
    
    #check for empty password; LDAP passes requests with empty passwords, we don't
    if(request_data['password'] == ""):
        json_data['message'] = 'Empty Password'
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response
    
    #attempt connection to ldap server
    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        handle = ldap.initialize("ldaps://dc-ad-gonzaga.gonzaga.edu")
        
        #attempt bind on user provided credentials with email @zagmail.gonzaga.edu
        try:
            handle.simple_bind_s(request_data['username'], request_data['password'])
            
            #if successful return OK, username+pwd is in the ldap database!
            json_data['message'] = 'Authentication succesful!'
            #checks if user is already in our database, assigns variable yes if so
            if User.objects.filter(username=user).exists():
                json_data['exists'] ='yes'
                json_data['first_name'] = User.objects.get(username=user).first_name
                json_data['last_name'] = User.objects.get(username=user).last_name
                json_data['p_email'] = User.objects.get(username=user).pref_email
                json_data['phone'] = User.objects.get(username=user).phone 
            else:
                json_data['exists'] ='no'
            json_data['username'] = user
            json_data['g_email'] = request_data['username']
            request_data = None #clear traces of user information after done using
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
            return response
        #catch exception, the zagmail suffix didn't work
        except ldap.LDAPError, error_message:
            #attempt bind on user provided credentials with email @gonzaga.edu
            try:
                #replace email suffix
                request_data['username'] = request_data['username'].replace('@zagmail.gonzaga.edu','@gonzaga.edu')
                
                #attempt bind with username and password gonzaga.edu
                handle.simple_bind_s(request_data['username'],request_data['password'])
                
                #if successful return OK, username+pwd is in the ldap database!
                json_data['message'] = 'Authentication succesful!'
                
                #checks if user is already in our database, assigns variable yes if so
                if User.objects.filter(username=user).exists():
                    json_data['exists'] ='yes'
                    json_data['first_name'] = User.objects.get(username=user).first_name
                    json_data['last_name'] = User.objects.get(username=user).last_name
                    json_data['p_email'] = User.objects.get(username=user).pref_email
                    json_data['phone'] = User.objects.get(username=user).phone
                    json_data['posts'] = post_list_views.user_posts(user)
                else:
                    json_data['exists'] ='no'
                json_data['username'] = user                   
                json_data['g_email'] = request_data['username']
                response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
                request_data = None #clear traces of user information after done using
                return response
            
            #catch exception, neither username+email_suffix+password in ldap database, return bad request
            except ldap.LDAPError, error_message:
                print error_message
                json_data['message'] = 'Invalid Credentials'
                response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
                request_data = None #clear traces of user information after done using
                return response
                
    #failure to connect to ldap server, return internal server error   
    except ldap.LDAPError, error_message:
        print error_message
        json_data['message'] = 'Error Connecting to Ldap Server'
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_500_INTERNAL_SERVER_ERROR,content_type='application/json')
        response.write(error_message)
        request_data = None #clear traces of user information after done using
        return response
        
@api_view(['POST'])
def user_posts(request):
    '''
    POST method for retrieving a set of posts belonging to a user in listview format
    the following elements must be included in the request body:
    username: username of user to have posts collected for
    '''
    json_data = {}
    try:
        #parse incoming request data, assign parameters
        request_data = ast.literal_eval(request.body)
        username = request_data['username']
        older = request_data['older']
        divider = request_data['divider_date_time']
        divider = divider.replace("\/","/")
        
        #get block of posts older or newer than divider
        json_data['posts'],json_data['more_exist'] = post_list_views.user_posts(username,divider,older)
        
        #if user recently had a post deleted set recent_post_deletion='1'
        user = User.objects.get(username=username)
        json_data['recent_post_deletion'] = str(int(user.recent_post_deletion))
        user.recent_post_deletion = False
        user.save()
        
        
        json_data['message'] = "successfully retrieved user posts"
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response
    except Exception,e:
        json_data["message"] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response


@api_view(['GET'])
def stats(request):
    '''
    GET method for retrieving the current set of usage statistics
    no parameters
    '''
    json_data = {}
    try:
        analytic = Analytics.objects.get(id=1)
        json_data['# Users'] = analytic.num_users
        json_data['# Items Posts'] = analytic.num_item_posts
        json_data['# Rideshare Posts'] = analytic.num_rideshare_posts
        json_data['# Events Posts'] = analytic.num_events_posts
        json_data['# Manually Deleted Posts'] = analytic.num_manually_deleted_posts
        json_data['# Deleted Reported Posts'] = analytic.num_deleted_reported_posts
        json_data['# Post Views'] = analytic.num_post_views
        json_data['message'] = "Go ZigZaga"
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response
        
    except Exception,e:
        json_data["message"] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        request_data = None #clear traces of user information after done using
        return response

