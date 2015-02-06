from rest_framework import status
from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost
from agora_rest_api.post_service import helpers
from agora_rest_api import settings
from rest_framework.decorators import api_view
from django.http import HttpResponse
from base64 import decodestring
import datetime
import json
import ast
import pytz

# -*- coding: utf-8 -*-
"""
Table of Contents:
    edit_post(request)
    edit_book_post(request_data,edit_post)
    edit_datelocation_post(request_data,edit_post)
    edit_rideshare_post(request_data,edit_post)
"""

time_zone_loc = pytz.timezone(settings.TIME_ZONE)
time_zone_utc = pytz.timezone('UTC')
date_time_format = "%m\/%d\/%Y %I:%M %p"

@api_view(['POST'])
def edit_post(request):
    '''  
    POST method for editing Post data
    route: /editpost/
    '''    
    json_data = {}
    json_data["message"] = ""
    try:
        request_data = ast.literal_eval(request.body)#parse data
        category = request_data["category"]
        if category in settings.item_categories:
            edit_post = ItemPost.objects.get(id=request_data['id'])
            edit_post.display_value = request_data['price']
        elif category in settings.book_categories:
            edit_post = BookPost.objects.get(id=request_data['id'])
            edit_post = edit_book_post(request_data,edit_post)
        elif category in settings.datelocation_categories:
            edit_post = DateLocationPost.objects.get(id=request_data['id'])
            edit_post = edit_datelocation_post(request_data,edit_post)
        elif category in settings.rideshare_categories:
            edit_post = RideSharePost.objects.get(id=request_data['id'])
            edit_post = edit_rideshare_post(request_data,edit_post)
        else:
            json_data["message"] = 'Error in Editing post: Invalid category'
            return HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')    
        
        edit_post.title = request_data['title']
        edit_post.price = request_data['price']
        edit_post.description = request_data['description']
        edit_post.call = request_data['call']
        edit_post.text = request_data['text']
        edit_post.pref_email = request_data['pref_email']
        edit_post.gonzaga_email = request_data['gonzaga_email']

        utc_now = time_zone_utc.localize(datetime.datetime.utcnow()) #get UTC now, timezone set to UTC
        now = time_zone_loc.normalize(utc_now) #normalize to local timezone

        edit_post.post_date_time = now
        
        imagesBase64Array = request_data['images'] #images array, each as base64 string
        imageURLsArray = [edit_post.image1,edit_post.image2,edit_post.image3] #placeholders for image URLs
        for i in range(len(imagesBase64Array)-1):  
            if imagesBase64Array[i] == "deleted":
                #Delete Image
                json_data["message"] = helpers.delete_imagefile(settings.IMAGES_ROOT + imageURLsArray[i])
                imageURLsArray[i] = ""
            elif imagesBase64Array[i] != "": #Image has been overwritten
                imageData = decodestring(imagesBase64Array[i]) #convert back to binary
                imageURLsArray[i] = category + "_" + request_data['id'] + "_" + str(i) + ".png" #unique filename
                imagePath = settings.IMAGES_ROOT + imageURLsArray[i] #full filepath
                imagefile = open(imagePath,"wb") #open
                imagefile.write(imageData) #write
            
        '''set post's image attributes as image URLs'''
        edit_post.image1 = imageURLsArray[0]            
        edit_post.image2 = imageURLsArray[1]
        edit_post.image3 = imageURLsArray[2]   
        edit_post.save()
        if json_data["message"] == "":
            json_data["message"] = "Successfully Edited Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')

    #catch all unhandled exceptions
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response   

def edit_book_post(request_data,edit_post):
    ''' 
    Edit post function for book specific attributes
    '''
    edit_post.isbn = request_data['isbn']
    edit_post.display_value = request_data['price']
    return edit_post
    
def edit_datelocation_post(request_data,edit_post):
    ''' 
    Edit post function for book specific attributes
    '''
    edit_post.location = request_data['location']
    split_date = request_data['date_time'].split(",")
    date_part_1 = split_date[0][0:-2]
    date_part_2 = split_date[0][-2:]
    full_date = date_part_1 + "20" + date_part_2 + split_date[1]
    input_date_time = datetime.datetime.strptime(full_date,date_time_format)
    edit_post.date_time = input_date_time
    edit_post.display_value = input_date_time
    return edit_post
    
def edit_rideshare_post(request_data,edit_post):
    ''' 
    Edit post function for book specific attributes
    '''
    split_date_1 = request_data['departure_date_time'].split(",")
    date_part_1 = split_date_1[0][0:-2]
    date_part_2 = split_date_1[0][-2:]  
    full_departure_date = date_part_1 + "20" + date_part_2 + split_date_1[1]
    return_date_time = None
    
    if int(request_data["round_trip"]):
        split_date_2 = request_data['return_date_time'].split(",")
        date_part_3 = split_date_2[0][0:-2]
        date_part_4 = split_date_2[0][-2:]
        full_return_date = date_part_3 + "20" + date_part_4 + split_date_2[1]
        return_date_time = datetime.datetime.strptime(full_return_date,date_time_format)
    departure_date_time = datetime.datetime.strptime(full_departure_date,date_time_format)
    trip_details = "From " + request_data["start_location"] + " To " + request_data["end_location"]
    edit_post.departure_date_time = departure_date_time

    edit_post.trip = trip_details
    edit_post.round_trip = int(request_data['round_trip'])
    edit_post.return_date_time = return_date_time
    edit_post.display_value = trip_details
    return edit_post