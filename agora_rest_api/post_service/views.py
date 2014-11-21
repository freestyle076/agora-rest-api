from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework import serializers
from models import BookPost, DateLocationPost, ItemPost, RideSharePost
from agora_rest_api.user_service.models import User
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
import json
import ast
import sys
from base64 import decodestring

# Create your views here.

item_categories = ['Electronics','Furniture','Appliances & Kitchen','Recreation']
book_category = ['Books']
rideshare_category = ['Rideshare']
datelocation_categories = ['Services','Events']

  

@api_view(['POST','GET'])
def create_post(request):
    #json dictionary to pass back data
    json_data = {}
    try:
        request_data = ast.literal_eval(request.body) #parse data
        category = request_data['category']
        if category in item_categories:
            return create_item_post(request_data,json_data)
        elif category in book_category:
            return create_book_post(request_data,json_data)
        elif category in datelocation_categories:
            return create_datelocation_post(request_data,json_data)
        elif category in rideshare_category:
            return create_rideshare_post(request_data,json_data)
        else:
            json_data = {'message': 'Error in creating post: Invalid category'}
            return HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
    except:
        #error occured in parsing data or assigning edits
        json_data = {'message': str(sys.exc_info()[0])}
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
def create_book_post(request_data,json_data):  
    this_user = User.objects.get(username=request_data['username'])
    gonzaga_email = pref_email = phoneNumber = ''
    if request_data['gonzaga_email'] == '1':
        gonzaga_email = this_user.gonzaga_email
    if request_data['pref_email'] == '1':
        pref_email = this_user.pref_email
    if request_data['phone'] == '1':
        phoneNumber = this_user.phone
    
    try:
        created_post = BookPost.objects.create(
            username=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            isbn=request_data['isbn'],
            gonzaga_email= gonzaga_email,
            pref_email=pref_email,
            phone=phoneNumber)
        created_post.save()
        json_data['message'] = "Succesfully created Book Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except:
        json_data['message'] = sys.exc_info()[0]
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response 
        
def create_datelocation_post(request_data,json_data):  
    this_user = User.objects.get(username=request_data['username'])
    gonzaga_email = pref_email = phoneNumber = ''
    if request_data['gonzaga_email'] == '1':
        gonzaga_email = this_user.gonzaga_email
    if request_data['pref_email'] == '1':
        pref_email = this_user.pref_email
    if request_data['phone'] == '1':
        phoneNumber = this_user.phone
    
    try:
        created_post = DateLocationPost.objects.create(
            username=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            date_time=request_data['date_time'],
            location=request_data['location'],
            gonzaga_email= gonzaga_email,
            pref_email=pref_email,
            phone=phoneNumber)
        created_post.save()
        json_data['message'] = "Succesfully created Book Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except:
        json_data['message'] = sys.exc_info()[0]
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response  
        
def create_rideshare_post(request_data,json_data):  
    this_user = User.objects.get(username=request_data['username'])
    gonzaga_email = pref_email = phoneNumber = ''
    if request_data['gonzaga_email'] == '1':
        gonzaga_email = this_user.gonzaga_email
    if request_data['pref_email'] == '1':
        pref_email = this_user.pref_email
    if request_data['phone'] == '1':
        phoneNumber = this_user.phone
    
    try:
        created_post = RideSharePost.objects.create(
            username=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            departure_date_time=request_data['departure_date_time'],
            trip=request_data['trip'],
            return_date_time = request_data['return_date_time'],
            round_trip = request_data['round_trip'],
            gonzaga_email= gonzaga_email,
            pref_email=pref_email,
            phone=phoneNumber)
        created_post.save()
        json_data['message'] = "Succesfully created Book Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except:
        json_data['message'] = sys.exc_info()[0]
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response  
        
def create_item_post(request_data,json_data):  
    this_user = User.objects.get(username=request_data['username'])
    gonzaga_email = pref_email =  ''
    phoneNumber = 1
    if request_data['gonzaga_email'] == '1':
        gonzaga_email = this_user.gonzaga_email
    if request_data['pref_email'] == '1':
        pref_email = this_user.pref_email
    if request_data['phone'] == '1':
        phoneNumber = this_user.phone
    try:
        print "create_book"
        created_post = ItemPost.objects.create(
            username=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            gonzaga_email= gonzaga_email,
            pref_email=pref_email,
            phone=phoneNumber)
        created_post.save()

        json_data['message'] = "Succesfully created Book Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except:
        json_data['message'] = sys.exc_info()[0]
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response    
         
@api_view(['POST'])
def upload_image(request):
    try:   
        request_data = ast.literal_eval(request.body)
        imagestr = request_data['image']
        print imagestr
        imagedata = decodestring(imagestr)
        imagefile = open("badass.png","wb")
        imagefile.write(imagedata)
        
        return HttpResponse(status=status.HTTP_200_OK,content_type='application/json')
    except:
        print str(sys.exc_info()[0])
        
def convert_hexstring_to_hex(hexstring):
    print "in convert"
    while hexstring != '':
        rgba = hexstring[0:8]    
        print hex(rgba)
        hexstring = hexstring[8:]
    
    
