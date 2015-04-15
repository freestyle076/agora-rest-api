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
date_time_format = "%m/%d/%y, %I:%M %p"

@api_view(['POST'])
def edit_post(request):
    '''  
    POST method for editing a generic post's data
    route: /editpost/
    '''    
    
    json_data = {}
    json_data["message"] = ""
    try:
        request_data = ast.literal_eval(request.body)#parse data
        
        #Gather post category and ID from request
        category = request_data["category"]
        post_id = int(request_data['post_id'])    
        
        #Find what table the post belongs to and edit category specific values
        if category in settings.item_categories:
            edit_post = ItemPost.objects.get(id=post_id)
            display_value_temp = request_data['price']
            if request_data['price']  == '':
                display_value_temp = ''
            #if price is 0 set display value to free
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
        
        #set temporary price value before assigning 
        price_temp = request_data['price']    
        if request_data['price']  == '':
            price_temp = None
        elif float(request_data['price']) == 0.:
            price_temp = 0.
            
        #Edit all generic post attributes    
        edit_post.title = request_data['title']
        edit_post.price = price_temp
        edit_post.description = request_data['description']
        edit_post.call = int(request_data['call'])
        edit_post.text = int(request_data['text'])
        edit_post.pref_email = int(request_data['pref_email'])
        edit_post.gonzaga_email = int(request_data['gonzaga_email'])
        
        #Edit image data
        imagesBase64Array = request_data['images'] #images array, each as base64 string
        imageURLsArray = [edit_post.image1,edit_post.image2,edit_post.image3] #placeholders for image URLs
        for i in range(len(imagesBase64Array)):  
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
                
        
        #Shifts any pictures that may have been deleted so all pictures are filled from left to right
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
                    
        #set post's image attributes as image URLs
        edit_post.image1 = imageURLsArray[0]            
        edit_post.image2 = imageURLsArray[1]
        edit_post.image3 = imageURLsArray[2]  

        #Save changes to post                
        edit_post.save()
        
        #Pass new posting time back to client
        json_data["post_date_time"] = edit_post.post_date_time.strftime('%m/%d/%Y %H:%M:%S')
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
    #if price is 0 set display value to free
    elif float(request_data['price']) == 0.:
        display_value_temp = 'Free'
        
    #Alter isbn and display value     
    edit_post.isbn = request_data['isbn']
    edit_post.display_value = display_value_temp
    return edit_post
    
def edit_datelocation_post(request_data,edit_post):
    ''' 
    Edit post function for datelocation post specific attributes
    '''
    edit_post.location = request_data['location']
    #Format date and time of event
    if request_data["date_time"]:
        input_date_time = request_data["date_time"].replace("\\","") #
        input_date_time = time_zone_utc.localize(datetime.datetime.strptime(input_date_time,date_time_format))          
    else:
        input_date_time = None
    #alter date_time and display value of event
    edit_post.date_time = input_date_time
    edit_post.display_value = input_date_time
    return edit_post
    
def edit_rideshare_post(request_data,edit_post):
    ''' 
    Edit post function for Rideshare post specific attributes
    '''
    #pre assign return_date_time to none in case there is no value provided
    return_date_time = None
    #Check if rideshare is round trip and assign round trip variables
    if int(request_data["round_trip"]):
        if request_data["return_date_time"]:
            return_date_time = request_data["return_date_time"].replace("\\","") 
            return_date_time = time_zone_utc.localize(datetime.datetime.strptime(return_date_time,date_time_format))          
    #assign departure time only if one is provided
    if request_data["departure_date_time"]:
        departure_date_time = request_data["departure_date_time"].replace("\\","") 
        departure_date_time = time_zone_utc.localize(datetime.datetime.strptime(departure_date_time,date_time_format))          
    else:
        departure_date_time = None    
    
    #trip details field
    trip_details = ""
    #if there is a start location provided then include start, check for end...
    if request_data["start_location"]:
        trip_details = trip_details + "From " + request_data["start_location"]
        if request_data["end_location"]:
            trip_details = trip_details + " To*& " + request_data["end_location"]
    #if there is no start location look to include end location only
    elif request_data["end_location"]:
        trip_details = trip_details + "To " + request_data["end_location"]
    
    #reassign all Rideshare post values
    edit_post.departure_date_time = departure_date_time
    edit_post.trip = trip_details
    edit_post.round_trip = int(request_data['round_trip'])
    edit_post.return_date_time = return_date_time
    
    if request_data["price"] == "":
        edit_post.display_value = ""
    #if price is 0 set display value to free
    elif float(request_data["price"]) == 0.:
        edit_post.display_value = "Free"
    else:
        edit_post.display_value = request_data["price"]
        
    return edit_post