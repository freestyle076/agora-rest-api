from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
import datetime
from agora_rest_api.user_service.models import User
from agora_rest_api.post_service.models import ItemPost, BookPost, DateLocationPost, RideSharePost
from agora_rest_api import settings
from rest_framework import status
from django.http import HttpResponse
from rest_framework.decorators import api_view
import json
import ast
import sys
from base64 import decodestring, encodestring
import pytz
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
# Create your views here.

item_categories = ['Electronics','Furniture','Appliances & Kitchen','Recreation','Clothing']
book_category = ['Books']
rideshare_category = ['Ride Shares']
datelocation_categories = ['Services','Events']

date_time_format = "%m\/%d\/%Y %I:%M %p"

@api_view(['POST'])
def view_detailed_post(request):
    '''
    POST method for retrieving detailed Post data to be viewed. 
    Request body must contain the following data in JSON format:
        postId: Identifier for what particular post to grab
        category: Category to signify which table to search through. 
    route: /viewpost/
    '''
    json_data = {}

    try:
        request_data = ast.literal_eval(request.body) #parse data
        category = request_data['category'] #switch on category
        post_id = request_data['post_id']
        if category in item_categories:
            post_info = ItemPost.objects.get(id=post_id)
        elif category in book_category:
            post_info = BookPost.objects.get(id=post_id)
        elif category in datelocation_categories:
            post_info = DateLocationPost.objects.get(id=post_id)
        elif category in rideshare_category:
            post_info = RideSharePost.objects.get(id=post_id)
        post_user = User.objects.get(username=post_info.username_id)
        json_data['title'] = post_info.title
        json_data['price'] = str(post_info.price)
        json_data['description'] = post_info.description
        if post_info.call == 1:
            json_data["call"] = post_user.phone
        else:
            json_data["call"] = ''
        if post_info.text == 1:
            json_data["text"] = post_user.phone
        else:
            json_data["text"] = ''
        if post_info.gonzaga_email == 1:
            json_data["gonzaga_email"] = post_user.gonzaga_email
        else:
            json_data["gonzaga_email"] = ''
        if post_info.pref_email == 1:
            json_data["pref_email"] = post_user.pref_email
        else:
            json_data["pref_email"] = ''
          
        image_URLs_array = ['','','']
        images_base64_array = ['','','']
        pre_image_string = 'agora_rest_api/media/images/'
        image_URLs_array[0] = pre_image_string + post_info.image1
        image_URLs_array[1] = pre_image_string + post_info.image2
        image_URLs_array[2] = pre_image_string + post_info.image3
        for i in range(len(image_URLs_array)):
            if image_URLs_array[i] != 'agora_rest_api/media/images/':
                image_file = open(image_URLs_array[i],"rb")
                image_data = image_file.read()
                images_base64_array[i] = encodestring(image_data)
                image_file.close()
      
        json_data["image1"] = images_base64_array[0]    
        json_data["image2"] = images_base64_array[1]    
        json_data["image3"] = images_base64_array[2]  
   
        if category in item_categories:
            return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        elif category in book_category:
            return view_book_post(request_data,json_data,post_info)
        elif category in datelocation_categories:
            return view_datelocation_post(request_data,json_data,post_info)
        elif category in rideshare_category:
            return view_rideshare_post(request_data,json_data,post_info)
        else:
            json_data = {'message': 'Error in viewing post: Invalid category'}
            return HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
    except Exception,e:
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
def view_book_post(request_data,json_data,Post):
    try:
        json_data["isbn"] = Post.isbn
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except Exception,e:
        print e
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response

def view_rideshare_post(request_data,json_data,Post):
    try:
        json_data["trip"] = Post.trip
        json_data["departure_date_time"] = str(Post.departure_date_time)
        if Post.round_trip:
            json_data["return_date_time"] = str(Post.return_date_time)
            json_data["round_trip"] = 1
        else:
            json_data["round_trip"] = 0
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except Exception,e:
        print e
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response

def view_datelocation_post(request_data,json_data,Post):
    try:
        json_data["date_time"] = str(Post.date_time)
        json_data["location"] = Post.location
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except Exception,e:
        print e
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
        
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
            call=request_data['call'],
            text=request_data['text'],
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
        json_data['message'] = "Succesfully created Book Post!"
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    #general exception catching
    except Exception,e:
        print e
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response 
        
def create_datelocation_post(request_data,json_data): 
    split_date = request_data['date_time'].split(",")
    date_part_1 = split_date[0][0:-2]
    date_part_2 = split_date[0][-2:]
    full_date = date_part_1 + "20" + date_part_2 + split_date[1]
    input_date_time = datetime.datetime.strptime(full_date,date_time_format)
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
            call=request_data['call'],
            text=request_data['text'],
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
    
    split_date_1 = request_data['departure_date_time'].split(",")
    date_part_1 = split_date_1[0][0:-2]
    date_part_2 = split_date_1[0][-2:]
    full_departure_date = date_part_1 + "20" + date_part_2 + split_date_1[1]
    split_date_2 = request_data['return_date_time'].split(",")
    date_part_3 = split_date_2[0][0:-2]
    date_part_4 = split_date_2[0][-2:]
    full_return_date = date_part_3 + "20" + date_part_4 + split_date_2[1]
    departure_date_time = datetime.datetime.strptime(full_departure_date,date_time_format)
    return_date_time = datetime.datetime.strptime(full_return_date,date_time_format)
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
            call=request_data['call'],
            text=request_data['text'],
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
            call=request_data['call'],
            text=request_data['text'],
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