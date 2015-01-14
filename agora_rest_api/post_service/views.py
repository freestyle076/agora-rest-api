from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
import datetime

from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost
from agora_rest_api.user_service.models import User
from agora_rest_api.post_service.models import ItemPost, BookPost, DateLocationPost, RideSharePost
from agora_rest_api import settings

from rest_framework import viewsets
from rest_framework import status
from rest_framework import status
from rest_framework.decorators import api_view

from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q

from base64 import decodestring
from base64 import encodestring

import datetime
import json
import ast
import sys
from base64 import decodestring, encodestring
import pytz
from django.core.context_processors import csrf
from django.shortcuts import render_to_response

import pytz

item_categories = ['Electronics','Furniture','Appliances & Kitchen','Recreation','Clothing']
book_category = ['Books']
rideshare_category = ['Ride Shares']
datelocation_categories = ['Services','Events']

date_time_format = "%m\/%d\/%Y %I:%M %p"

# Create your views here.
def prepare_results(items, books, DLs, RSs):
    '''
    Prepares a list a filter request results, each in listview post format.
    Returns a list of objects, ready to be included in a JSON object.
    items: ItemPost resultset
    books: BookPost resultset
    DLs: DateLocationPost resultset
    RSs: RidesharePost resultset
    
    '''
    posts = []

    #items    
    for item in items:
        image = open(str(item.image1),'rb').read()
        imageString = encodestring(image) #encode image data as string for port of JSON
        listview_item = {'id':item.id,'title':item.title,'category':item.category,'display_value':item.display_value,'image':imageString}
        posts.append(listview_item)
        
    #books
    for book in books:
        image = open(str(book.image1),'rb').read()
        imageString = encodestring(image) #encode image data as string for port of JSON
        listview_book = {'id':book.id,'title':book.title,'category':book.category,'display_value':book.display_value,'image':imageString}
        posts.append(listview_book)
    
    #Datelocations
    for DL in DLs:
        image = open(str(DL.image1),'rb').read()
        imageString = encodestring(image) #encode image data as string for port of JSON
        listview_DL = {'id':DL.id,'title':DL.title,'category':DL.category,'display_value':DL.display_value,'image':imageString}
        posts.append(listview_DL)
    
    #Rideshares
    for RS in RSs:
        image = open(str(RS.image1),'rb').read()
        imageString = encodestring(image) #encode image data as string for port of JSON
        listview_RS = {'id':RS.id,'title':RS.title,'category':RS.category,'display_value':RS.display_value,'image':imageString}
        posts.append(listview_RS)
        
    #now posts is a list of all posts that made the cut in listview format    
    
    return posts

@api_view(['POST'])
def filter_post_list(request):
    '''
    GET method for retrieving list of List View Post data to be viewed. 
    Request body must contain the following data in JSON format:
        category: Category filter, member of collection of lowest level categories
        keyword: Keyword search string. To be applied to any attributes that make sense
                    (as opposed to not making sense).
        min_price: Minimum price filter
        max_price: Maximum price filter
        free: Free items only flag. Sets min_price,max_price = 0
    route: /postquery/
    '''
    json_data = {}
    try:
        #get filter parameters from request
        request_data = ast.literal_eval(request.body)
        keyword = request_data['keyword']
        _category = request_data['category']
        max_price = float(request_data['max_price'])
        min_price = float(request_data['min_price'])
        free = bool(request_data['free'])
        
        #clean keyword input
        keyword.strip() #removing leading or trailing whitespace        
        
        #min_price and max_price not specified
        if not max_price:
            max_price = 10000.
        if not min_price:
            min_price = 0.
        
        #react to free flag
        if free:
            max_price = 0.
            min_price = 0.        
        
        #set active categories---------------
        
        #in a populate as necessary sort of way...
        item_rs = None
        book_rs = None
        DL_rs = None
        RS_rs = None
        
        #if no chosen category apply all
        if not _category:
            item_rs = get_item_result_set()
            book_rs = get_book_resul_set()
            DL_rs = get_DL_result_set()
            RS_rs = get_RS_result_set()
            
        #category is of item type
        elif category in item_categories:
            #keyword applied to display_value, title, description
            item_rs = ItemPost.objects.filter(category__iexact=_category, Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword), price__gte=min_price, price_lte=max_price)
            
        #category is of book type
        elif category in book_categories:
            #keyword applied to display_value, title, description, isbn            
            book_rs = BookPost.objects.filter(category__iexact=_category,Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) |Q(isbn__icontains=keyword), price__gte=min_price, price_lte=max_price)
            
        #category is of book type
        elif category in datelocation_categories:
            #keyword applied to display_value, title, description, location
            DL_rs = DateLocationPost.objects.filter(category__iexact=_category,Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(location__icontains=keyword), price__gte=min_price, price_lte=max_price)
            
        #category is of book type
        elif category in rideshare_categories:
            #keyword applied to display_value, title, description, trip
            RS_rs = RideSharePost.objects.filter(category__iexact=_category,Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(trip__icontains=keyword), price__gte=min_price, price_lte=max_price)
            
        #populate the response with listview formatted results (grabs and encodes image data)
        json_data['posts'] = prepare_results(items, books, DLs,RSs)                    
        
        #hi five
        json_data['message'] = 'Successfully filtered and returned posts'
        
        print json_data
        
        #respond with json and 200 OK
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        return response
    
    #catch all unhandled exceptions
    except Exception,e:
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response

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
        pre_image_string = settings.IMAGES_ROOT
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
    
    #catch all unhandled exceptions
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
    
    #catch all unhandled exceptions
    except Exception,e:
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