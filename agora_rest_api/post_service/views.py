from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
import datetime
from models import BookPost, DateLocationPost, ItemPost, RideSharePost
from agora_rest_api.user_service.models import User
from agora_rest_api import settings
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
import json
import ast
import sys
from base64 import decodestring
import pytz

# Create your views here.

item_categories = ['Electronics','Furniture','Appliances & Kitchen','Recreation','Clothing']
book_category = ['Books']
rideshare_category = ['Rideshare']
datelocation_categories = ['Services','Events']

date_time_format = "%d %m %Y %H"

@api_view(['POST'])
def create_post(request):
    #json dictionary to pass back data
    json_data = {}
    try:
        request_data = ast.literal_eval(request.body) #parse data
        category = request_data['category'] #switch on category
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
    except Exception,e:
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
def create_book_post(request_data,json_data):
    now = datetime.datetime.now(pytz.timezone('US/Pacific'))
    try:
        '''partially create post, hold for images'''
        created_post = BookPost.objects.create(
            username_id=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            isbn=request_data['isbn'],
            gonzaga_email= request_data['gonzaga_email'],
            pref_email=request_data['pref_email'],
            phone=request_data['phone'],
            display_value = int(request_data['price']),
            post_date_time = now)
            
        '''read images from request, format URLs and save images on disc'''
        ID = created_post.id #id of the partially created post
        image_root = settings.IMAGES_ROOT #images folder path
        imagesBase64Array = request_data['images'] #images array, each as base64 string
        imageURLsArray = ['','',''] #placeholders for image URLs
        for i in range(len(imagesBase64Array)):
            imageData = decodestring(imagesBase64Array[i]) #convert back to binary
            imageURLsArray[i] = request_data['category'] + "_" + str(ID) + "_" + str(i) + ".png" #unique filename
            imagePath = image_root + imageURLsArray[i] #full filepath
            imagefile = open(imagePath,"wb") #open
            imagefile.write(imageData) #write
        
        '''set post's image attributes as image URLs'''
        created_post.image1 = imageURLsArray[0]            
        created_post.image2 = imageURLsArray[1]
        created_post.image3 = imageURLsArray[2]              
        
        '''save and respond with success'''
        created_post.save()
        json_data['message'] = "Succesfully created Book Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except Exception,e:
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response 
        
def create_datelocation_post(request_data,json_data): 
    input_date_time = datetime.datetime.strptime(request_data['date_time'],date_time_format)
    now = datetime.datetime.now(pytz.timezone('US/Pacific'))
    try:
        '''partially create post, hold for images'''
        created_post = DateLocationPost.objects.create(
            username_id=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            date_time=input_date_time,
            location=request_data['location'],
            gonzaga_email= request_data['gonzaga_email'],
            pref_email=request_data['pref_email'],
            phone=request_data['phone'],
            display_value = input_date_time,
            post_date_time = now)
            
        '''read images from request, format URLs and save images on disc'''
        ID = created_post.id #id of the partially created post
        image_root = settings.IMAGES_ROOT #images folder path
        imagesBase64Array = request_data['images'] #images array, each as base64 string
        imageURLsArray = ['','',''] #placeholders for image URLs
        for i in range(len(imagesBase64Array)):
            imageData = decodestring(imagesBase64Array[i]) #convert back to binary
            imageURLsArray[i] = request_data['category'] + "_" + str(ID) + "_" + str(i) + ".png" #unique filename
            imagePath = image_root + imageURLsArray[i] #full filepath
            imagefile = open(imagePath,"wb") #open
            imagefile.write(imageData) #write
        
        '''set post's image attributes as image URLs'''
        created_post.image1 = imageURLsArray[0]            
        created_post.image2 = imageURLsArray[1]
        created_post.image3 = imageURLsArray[2]              
        
        '''save and respond with success'''
        created_post.save()
        json_data['message'] = "Succesfully created Date_location Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except Exception,e:
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response  
        
def create_rideshare_post(request_data,json_data):  
    departure_date_time = datetime.datetime.strptime(request_data['departure_date_time'],date_time_format)
    return_date_time = datetime.datetime.strptime(request_data['return_date_time'],date_time_format)
    trip_details = "From " + request_data["start_location"] + " To " + request_data["end_location"]
    now = datetime.datetime.now(pytz.timezone('US/Pacific'))
    try:
        '''partially create post, hold for images'''
        created_post = RideSharePost.objects.create(
            username_id=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            departure_date_time=departure_date_time,
            trip=trip_details,
            return_date_time = return_date_time,
            round_trip = request_data['round_trip'],
            gonzaga_email= request_data['gonzaga_email'],
            pref_email=request_data['pref_email'],
            phone=request_data['phone'],
            display_value = trip_details,
            post_date_time = now)
            
        '''read images from request, format URLs and save images on disc'''
        ID = created_post.id #id of the partially created post
        image_root = settings.IMAGES_ROOT #images folder path
        imagesBase64Array = request_data['images'] #images array, each as base64 string
        imageURLsArray = ['','',''] #placeholders for image URLs
        for i in range(len(imagesBase64Array)):
            imageData = decodestring(imagesBase64Array[i]) #convert back to binary
            imageURLsArray[i] = request_data['category'] + "_" + str(ID) + "_" + str(i) + ".png" #unique filename
            imagePath = image_root + imageURLsArray[i] #full filepath
            imagefile = open(imagePath,"wb") #open
            imagefile.write(imageData) #write
        
        '''set post's image attributes as image URLs'''
        created_post.image1 = imageURLsArray[0]            
        created_post.image2 = imageURLsArray[1]
        created_post.image3 = imageURLsArray[2]              
        
        '''save and respond with success'''
        created_post.save()
        json_data['message'] = "Succesfully created RideShare Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except Exception,e:
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response  
        
def create_item_post(request_data,json_data):
    now = datetime.datetime.now(pytz.timezone('US/Pacific'))
    try:
        '''partially create post, hold for images'''
        created_post = ItemPost.objects.create(
            username_id=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            gonzaga_email= request_data['gonzaga_email'],
            pref_email=request_data['pref_email'],
            phone=request_data['phone'],
            display_value = request_data['price'],
            post_date_time = now)
        
        '''read images from request, format URLs and save images on disc'''
        ID = created_post.id #id of the partially created post
        image_root = settings.IMAGES_ROOT #images folder path
        imagesBase64Array = request_data['images'] #images array, each as base64 string
        imageURLsArray = ['','',''] #placeholders for image URLs
        for i in range(len(imagesBase64Array)):
            imageData = decodestring(imagesBase64Array[i]) #convert back to binary
            imageURLsArray[i] = request_data['category'] + "_" + str(ID) + "_" + str(i) + ".png" #unique filename
            imagePath = image_root + imageURLsArray[i] #full filepath
            imagefile = open(imagePath,"wb") #open
            imagefile.write(imageData) #write
        
        '''set post's image attributes as image URLs'''
        created_post.image1 = imageURLsArray[0]            
        created_post.image2 = imageURLsArray[1]
        created_post.image3 = imageURLsArray[2]              
        
        '''save and respond with success'''
        created_post.save()
        json_data['message'] = "Succesfully created Item Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except Exception,e:
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response