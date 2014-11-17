from django.shortcuts import render
from models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from serializers import UserSerializer
from django.http import HttpResponse
from django.db import utils
from django.core import validators
from rest_framework.decorators import api_view
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import ldap
import json
import ast
import sys

# Create your views here.

item_categories = ['Electronics','Furniture','Appliances & Kitchen','Recreation']
book_category = ['Books']
rideshare_category = ['Rideshare']
datelocation_categories = ['Services','Events']

def create_item_post(request_data):
    return 0
    
def create_book_post(request_data):
    return 0

def create_datelocation_post(request_data):
    return 0
    
def create_rideshare_post(request_data):
    return 0    

@api_view(['POST'])
def create_post(request):
    try:
        request_data = ast.literal_eval(request.body) #parse data
        category = request_data['category']
        if category in item_categories:
            return create_item_post(request_data)
        elif category in book_category:
            return create_book_post(request_data)
        elif category in datelocation_categories:
            return create_datelocation_post(request_data)
        elif category in rideshare_category:
            return create_rideshare_post(request_data)
        else:
            json_data = {'message': 'Error in creating post: Invalid category'}
            return HttpResponse(json.dumps(json_data),status=HTTP_400_BAD_REQUEST,content_type='application/json')
    except:
        #error occured in parsing data or assigning edits
        json_data = {'message': str(sys.exc_info()[0])}
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response