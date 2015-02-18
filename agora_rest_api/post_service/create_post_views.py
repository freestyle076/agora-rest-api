from rest_framework import status
from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost
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
    create_post(request)
    create_book_post(request_data,json_data)
    create_datelocation_post(request_data,json_data)
    create_rideshare_post(request_data,json_data)
    create_item_post(request_data,json_data)
"""

time_zone_loc = pytz.timezone(settings.TIME_ZONE)
time_zone_utc = pytz.timezone('UTC')
date_time_format = "%m/%d/%y, %I:%M %p"


@api_view(['POST'])
def create_post(request):
    '''
    POST method for creating any post
    Request body must contain the following data in JSON format:
        title: title for particular post
        category: category of post being created
        username_id: ID for user that created post
        description: String describing the object to be sold
        price: float value signifying the desired price of object
        gonzaga_email: Boolean whether the poster desires to be contacted through gonzaga_email
        pref_email: Boolean whether the poster desires to be contacted through preferred email
        call: Boolean whether the poster desires to be contacted by a call
        text: Boolean whether the poster desires to be contacted by a text
        image1: Default image
        image2: Second image
        image3: Third image
    '''
    #json dictionary to pass back data
    json_data = {}
    try:
        request_data = ast.literal_eval(request.body) #parse data

        if request_data["price"] == '':
            request_data["price"] = 0
        category = request_data['category'] #switch on category
        if category in settings.item_categories: 
            return create_item_post(request_data,json_data)
        elif category in settings.book_categories:
            return create_book_post(request_data,json_data)
        elif category in settings.datelocation_categories:
            return create_datelocation_post(request_data,json_data)
        elif category in settings.rideshare_categories:
            return create_rideshare_post(request_data,json_data)
        else:
            json_data = {'message': 'Error in creating post: Invalid category'}
            return HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
    
    #catch all unhandled exceptions
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
def create_book_post(request_data,json_data):
    '''
    POST method for creating a book  post
    Request body must contain the following data in JSON format:
        isbn: isbn of book to be sold
    '''
    
    utc_now = time_zone_utc.localize(datetime.datetime.utcnow()) #get UTC now, timezone set to UTC  
    now = time_zone_loc.normalize(utc_now) #normalize to local timezone
    print "Book now: " + str(now)
    
    try:
        '''partially create post, hold for images'''
        created_post = BookPost.objects.create(
            username_id=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            isbn=request_data['isbn'],
            gonzaga_email= int(request_data['gonzaga_email']),
            pref_email=int(request_data['pref_email']),
            call=int(request_data['call']),
            text=int(request_data['text']),
            display_value = request_data['price'],
            post_date_time = now)
            
        '''read images from request, format URLs and save images on disc'''
        ID = created_post.id #id of the partially created post
        json_data['id'] = ID
        image_root = settings.IMAGES_ROOT #images folder path
        imagesBase64Array = request_data['images'] #images array, each as base64 string
        imageURLsArray = ['','',''] #placeholders for image URLs
        pictureIndex = 0
        for i in range(len(imagesBase64Array)):
            if imagesBase64Array[i] != '':
                pictureIndex = pictureIndex + 1
            imageData = decodestring(imagesBase64Array[i]) #convert back to binary
            imageURLsArray[pictureIndex] = request_data['category'] + "_" + str(ID) + "_" + str(pictureIndex) + ".png" #unique filename
            imagePath = image_root + imageURLsArray[pictureIndex] #full filepath
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
    
    #catch all unhandled exceptions
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
def create_datelocation_post(request_data,json_data):
    '''
    POST method for creating any post
    Request body must contain the following data in JSON format:
        date_time: Date and Time of event or service desired
        location: Location of event or service
    '''
    
    #inputted date_time for answer to event/service when?
    input_date_time = time_zone_utc.localize(datetime.datetime.strptime(request_data["date_time"],date_time_format))
    
    #for post_date_time (time created)
    utc_now = time_zone_utc.localize(datetime.datetime.utcnow()) #get UTC now, timezone set to UTC
    now = time_zone_loc.normalize(utc_now) #normalize to local timezone
    
    print "DL now: " + str(now)

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
            gonzaga_email= int(request_data['gonzaga_email']),
            pref_email=int(request_data['pref_email']),
            call=int(request_data['call']),
            text=int(request_data['text']),
            display_value = input_date_time,
            post_date_time = now)
            
        '''read images from request, format URLs and save images on disc'''
        ID = created_post.id #id of the partially created post

        json_data['id'] = ID
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
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response  
        
def create_rideshare_post(request_data,json_data): 
    '''
    POST method for creating a rideshare post
    Request body must contain the following data in JSON format:
        start_location: Beginning place of rideshare
        end_location: End place of rideshare
        round_trip: Boolean Value signifying 
        departure_date_time: date and time of departure
        return_date_time: date and time of return if it is a round trip
    '''
    
    '''
    return_date_time = None
    '''
    
    #preprocess incoming departure date time string
    departure_dt_string = request_data["departure_date_time"]
    departure_dt_string = departure_dt_string.replace("\\","") #remove unnecessary escapes
    
    #departure datetime object
    departure_date_time = time_zone_utc.localize(datetime.datetime.strptime(departure_dt_string,date_time_format))
    
    #handle return date time if round_trip is set    
    return_date_time = None
    if int(request_data["round_trip"]):

        #preprocess incoming return date time string
        return_dt_string = request_data["return_date_time"]
        return_dt_string = return_dt_string.replace("\\","") #remove unnecessary escapes
      
        
        #departure datetime object
        return_date_time = time_zone_utc.localize(datetime.datetime.strptime(return_dt_string,date_time_format))
    
    #trip details field
    trip_details = "From " + request_data["start_location"] + " To " + request_data["end_location"]
    
    #default display value to trip details
    display_value_temp = trip_details
    

    #if start or end not set display value becomes price
    if not request_data["start_location"] or not request_data["end_location"]:
        display_value_temp = request_data["price"]
    
    #for post_date_time
    utc_now = time_zone_utc.localize(datetime.datetime.utcnow()) #get UTC now, timezone set to UTC
    now = time_zone_loc.normalize(utc_now) #normalize to local timezone
    
    print "Created RS now: " + str(now)
    
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
            round_trip = int(request_data['round_trip']),
            gonzaga_email= int(request_data['gonzaga_email']),
            pref_email=int(request_data['pref_email']),
            call=int(request_data['call']),
            text=int(request_data['text']),
            display_value = display_value_temp,
            post_date_time = now)   
        '''read images from request, format URLs and save images on disc'''
 
        ID = created_post.id #id of the partially created post
        json_data['id'] = ID
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
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response  
        
def create_item_post(request_data,json_data):
    '''
    POST method for creating an item post
    '''

    #for post_date_time
    utc_now = time_zone_utc.localize(datetime.datetime.utcnow()) #get UTC now, timezone set to UTC
    now = time_zone_loc.normalize(utc_now) #normalize to local timezone
    
    print "item now: " + str(now)
    
    try:
        '''partially create post, hold for images'''
        created_post = ItemPost.objects.create(
            username_id=request_data['username'],
            title=request_data['title'],
            price=request_data['price'],
            category=request_data['category'],
            description=request_data['description'],
            gonzaga_email= int(request_data['gonzaga_email']),
            pref_email=int(request_data['pref_email']),
            call=int(request_data['call']),
            text=int(request_data['text']),
            display_value = request_data['price'],
            post_date_time = now)
        '''read images from request, format URLs and save images on disc'''
        ID = created_post.id #id of the partially created post
        json_data['id'] = ID
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
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response