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
date_time_format = "%m\/%d\/%y, %I:%M %p"

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

        print request_data["images"][1]      
        if request_data["images"][1] == None:
            print ";asdfhas;djfhas"
        else:
            print "something"
        
        
        category = request_data["category"]
        post_id = int(request_data['post_id'])

        print 'category: ' + category
        print 'post_id: ' + str(post_id)       
        
        if category in settings.item_categories:
            edit_post = ItemPost.objects.get(id=post_id)
            display_value_temp = request_data['price']
            if request_data['price']  == '':
                display_value_temp = ''
            elif float(request_data['price']) == 0.:
                display_value_temp = 'Free'
            edit_post.display_value = display_value_temp
        elif category in settings.book_categories:
            edit_post = BookPost.objects.get(id=post_id)
            edit_post = edit_book_post(request_data,edit_post)
        elif category in settings.datelocation_categories:
            edit_post = DateLocationPost.objects.get(id=post_id)
            edit_post = edit_datelocation_post(request_data,edit_post)
        elif category in settings.rideshare_categories:
            edit_post = RideSharePost.objects.get(id=post_id)
            edit_post = edit_rideshare_post(request_data,edit_post)
        else:
            json_data["message"] = 'Error in Editing post: Invalid category'
            return HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json') 
        
        price_temp = request_data['price']    
        if request_data['price']  == '':
            price_temp = None
        elif float(request_data['price']) == 0.:
            price_temp = 0.
            
        edit_post.title = request_data['title']
        edit_post.price = price_temp
        edit_post.description = request_data['description']
        edit_post.call = int(request_data['call'])
        edit_post.text = int(request_data['text'])
        edit_post.pref_email = int(request_data['pref_email'])
        edit_post.gonzaga_email = int(request_data['gonzaga_email'])
        
        imagesBase64Array = request_data['images'] #images array, each as base64 string
        imageURLsArray = [edit_post.image1,edit_post.image2,edit_post.image3] #placeholders for image URLs
        for i in range(len(imagesBase64Array)-1):  
            if imagesBase64Array[i] == "deleted":
                #Delete Image
                json_data["message"] = helpers.delete_imagefile(settings.IMAGES_ROOT + imageURLsArray[i])
                imageURLsArray[i] = ""
            elif imagesBase64Array[i] != "": #Image has been overwritten
                imageData = decodestring(imagesBase64Array[i]) #convert back to binary
                imageURLsArray[i] = category + "_" + str(post_id) + "_" + str(i) + ".png" #unique filename
                imagePath = settings.IMAGES_ROOT + imageURLsArray[i] #full filepath
                imagefile = open(imagePath,"wb") #open
                imagefile.write(imageData) #write
                
        print imageURLsArray[1] + " <------"
        
        '''Shifts any pictures that may have been deleted so all pictures are filled from left to right'''
        for j in range(2):                   
            for i in range(1,3):
                if imageURLsArray[i] != '':
                    if imageURLsArray[i - 1] == '':
                        imageURLsArray[i - 1] = category + "_" + str(post_id) + "_" + str(i - 1) + ".png" #unique filename 
                        oldImagePath = settings.IMAGES_ROOT + imageURLsArray[i] #full filepath
                        oldImageFile = open(oldImagePath,"rb") #open
                        oldImageData = oldImageFile.read()
                        newImagePath = settings.IMAGES_ROOT + imageURLsArray[i - 1] #full filepath
                        newImageFile = open(newImagePath,"wb")
                        newImageFile.write(oldImageData)
                        json_data["message"] = helpers.delete_imagefile(oldImagePath)
                        imageURLsArray[i] = ""
                    
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
    display_value_temp = request_data['price']
    if request_data['price']  == '':
        display_value_temp = ''
    elif float(request_data['price']) == 0.:
        display_value_temp = 'Free'
        
    edit_post.isbn = request_data['isbn']
    edit_post.display_value = display_value_temp
    return edit_post
    
def edit_datelocation_post(request_data,edit_post):
    ''' 
    Edit post function for book specific attributes
    '''
    edit_post.location = request_data['location']
    input_date_time = datetime.datetime.strptime(request_data['date_time'],date_time_format)
    edit_post.date_time = input_date_time
    edit_post.display_value = input_date_time
    return edit_post
    
def edit_rideshare_post(request_data,edit_post):
    ''' 
    Edit post function for book specific attributes
    '''
    
    return_date_time = None
    
    if int(request_data["round_trip"]):
        return_date_time = datetime.datetime.strptime(request_data['return_date_time'],date_time_format)
    departure_date_time = datetime.datetime.strptime(request_data['departure_date_time'],date_time_format)
    trip_details = "From " + request_data["start_location"] + " To " + request_data["end_location"]
    edit_post.departure_date_time = departure_date_time

    edit_post.trip = trip_details
    edit_post.round_trip = int(request_data['round_trip'])
    edit_post.return_date_time = return_date_time
    edit_post.display_value = trip_details
    return edit_post