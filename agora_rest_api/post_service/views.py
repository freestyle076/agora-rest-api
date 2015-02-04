from rest_framework import status
from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost, PostReport
from agora_rest_api.user_service.models import User
from agora_rest_api import settings
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.db.models import Q
from base64 import decodestring
from base64 import encodestring
import datetime
import json
import ast
import pytz
import os

item_categories = ['Electronics','Household','Recreation','Clothing']
book_categories = ['Books']
rideshare_categories = ['Ride Shares']
datelocation_categories = ['Services','Events']

date_time_format = "%m\/%d\/%Y %I:%M %p"

def delete_imagefile(filename):
    json_data = {}
    try:
        if os.path.isfile(filename):
            os.remove(filename)
        else:
            json_data["message"] = ("Error: %s file  not found" % filename)
            return json_data["message"]
    except Exception,e:
        print str(e)
        json_data["message"] = str(e)   
        return json_data["message"]
        
        
def remove_post(delete_post):
    json_data = {}
    json_data["message"] = ""
    try:
        imageURLsArray = [delete_post.image1,delete_post.image2,delete_post.image3] #placeholders for image URLs
        for i in range(len(imageURLsArray)):  
            if imageURLsArray[i] != "":
                #Delete Image
                json_data["message"] = delete_imagefile(settings.IMAGES_ROOT + imageURLsArray[i])
                imageURLsArray[i] = ""                
        post_reports = PostReport.objects.filter(post_id=delete_post.id)
        for post in post_reports:
            post.delete()
        delete_post.delete()
        return json_data["message"]
    except Exception,e:
        print str(e)
        json_data["message"] = str(e) 
        return json_data["message"]
        
        
@api_view(['POST'])
def delete_post(request):
    '''  
    POST method for deleting a Post and its images
    route: /deletepost/
    '''
    json_data = {}
    try:
        request_data = ast.literal_eval(request.body)#parse data
        category = request_data["category"]
        if category in item_categories:
            delete_post = ItemPost.objects.get(id=request_data['id'])
        elif category in book_categories:
            delete_post = BookPost.objects.get(id=request_data['id'])
        elif category in datelocation_categories:
            delete_post = DateLocationPost.objects.get(id=request_data['id'])
        elif category in rideshare_categories:
            delete_post = RideSharePost.objects.get(id=request_data['id'])
        else:
            json_data = {'message': 'Error in Editing post: Invalid category'}
            return HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')    
        json_data["message"] = remove_post(delete_post)
        if json_data["message"] == "":
            json_data['message'] = "Succesfully Deleted Post"   
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    
    #catch all unhandled exceptions
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response    
        
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
        if category in item_categories:
            edit_post = ItemPost.objects.get(id=request_data['id'])
            edit_post.display_value = request_data['price']
        elif category in book_categories:
            edit_post = BookPost.objects.get(id=request_data['id'])
            edit_post = edit_book_post(request_data,edit_post)
        elif category in datelocation_categories:
            edit_post = DateLocationPost.objects.get(id=request_data['id'])
            edit_post = edit_datelocation_post(request_data,edit_post)
        elif category in rideshare_categories:
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
        now = datetime.datetime.now(pytz.timezone('US/Pacific'))
        edit_post.post_date_time = now
        
        imagesBase64Array = request_data['images'] #images array, each as base64 string
        imageURLsArray = [edit_post.image1,edit_post.image2,edit_post.image3] #placeholders for image URLs
        for i in range(len(imagesBase64Array)-1):  
            if imagesBase64Array[i] == "deleted":
                #Delete Image
                json_data["message"] = delete_imagefile(settings.IMAGES_ROOT + imageURLsArray[i])
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
    
def user_posts(username):
    '''
    Gathers an aggregate list of posts, in listview format, that belong to
    the user whose username matches parameter username
    username: user whose posts will be collected
    '''
    print "inside user posts"
    
    try:

        #collect posts belonging to the user
        item_rs = ItemPost.objects.filter(Q(username_id__exact=username))
        book_rs = BookPost.objects.filter(Q(username_id__exact=username))
        DL_rs = DateLocationPost.objects.filter(Q(username_id__exact=username))
        RS_rs = RideSharePost.objects.filter(Q(username_id__exact=username))
        
        #prepare the results: listview format in order of post date        
        return prepare_results(item_rs,book_rs,DL_rs,RS_rs)
    
    #general exception handling
    except Exception, e:
        raise e
        

def prepare_results(items, books, DLs, RSs, limit=0):
    '''
    Prepares a list a filter request results, each in listview post format.
    Returns a list of objects, ready to be included in a JSON object.
    items: ItemPost resultset
    books: BookPost resultset
    DLs: DateLocationPost resultset
    RSs: RidesharePost resultset
    '''
    print "inside prepare_results"     
    
    posts = []
    
    try:
        #items
        if items:  
            for item in items:
                if item.image1:
                    image = open(settings.IMAGES_ROOT + str(item.image1),'rb').read()
                    imageString = encodestring(image) #encode image data as string for port of JSON
                else:
                    imageString = ''
                decorated_price = "${:.2f}".format(float(item.price))
                listview_item = {'id':item.id,'title':item.title,'category':item.category,'display_value':decorated_price,'image':imageString,'post_date_time':item.post_date_time.strftime('%m/%d/%Y %H:%M:%S')}
                posts.append(listview_item)
                
                
        #books
        if books:
            for book in books:
                if book.image1:
                    image = open(settings.IMAGES_ROOT + str(book.image1),'rb').read()
                    imageString = encodestring(image) #encode image data as string for port of JSON
                else:
                    imageString = ''
                decorated_price = "${:.2f}".format(float(book.price))
                listview_book = {'id':book.id,'title':book.title,'category':book.category,'display_value':decorated_price,'image':imageString,'post_date_time':book.post_date_time.strftime('%m/%d/%Y %H:%M:%S')}
                posts.append(listview_book)


        #Datelocations
        if DLs:
            for DL in DLs:
                if DL.image1:
                    image = open(settings.IMAGES_ROOT + str(DL.image1),'rb').read()
                    imageString = encodestring(image) #encode image data as string for port of JSON
                else:
                    imageString = ''
                month = str(DL.date_time.month) #month without leading zero
                hour = str((DL.date_time.hour) % 12) #hour without leading zero
                day = str(DL.date_time.day)
                if hour == "0": #weird attribute of time-keeping, 0 is actually 12
                    hour = "12"
                year = DL.date_time.strftime("/%y") #day and year component
                minute_ampm = DL.date_time.strftime(":%M%p") #minute and am/pm component
                
                #pretty_date = DL.date_time.strftime("%m/%d/%y %I:%M%p") #modify the datetime to be a bit prettier
                pretty_date = month + "/" + day + "/" + year + " " + hour + minute_ampm                 
                
                listview_DL = {'id':DL.id,'title':DL.title,'category':DL.category,'display_value':pretty_date,'image':imageString,'post_date_time':DL.post_date_time.strftime('%m/%d/%Y %H:%M:%S')}
                posts.append(listview_DL)


        #Rideshares
        if RSs:
            for RS in RSs:
                if RS.image1:
                    image = open(settings.IMAGES_ROOT + str(RS.image1),'rb').read()
                    imageString = encodestring(image) #encode image data as string for port of JSON
                else:
                    imageString = ''
                listview_RS = {'id':RS.id,'title':RS.title,'category':RS.category,'display_value':RS.display_value,'image':imageString,'post_date_time':RS.post_date_time.strftime('%m/%d/%Y %H:%M:%S')}
                posts.append(listview_RS)
                                     


        def datetime_key(datetime_string):
            """
            Post sorting helper function to provide a sortable attribute
            datetime_string: datetime in formatted string (see global variable date_time_format)
            """
            datetime_obj = datetime.datetime.strptime(datetime_string,'%m/%d/%Y %H:%M:%S')
            return datetime_obj
    
         
        #sort the list of posts on their post_date_time attribute
        posts.sort(key=lambda x: datetime_key(x['post_date_time']),reverse=True)
        
        
        if limit > 0:
            posts = posts[:limit]
        
        print "Number of posts: " + str(len(posts))        
        
        return posts
        
    #ensure that exceptions are raised to the point of being included in the http response
    except Exception, e:
        raise e


@api_view(['POST'])
def filter_post_list(request):
    '''
    POST method for retrieving list of List View Post data to be viewed. 
    Request body must contain the following data in JSON format:
        category: Category filter, member of collection of lowest level categories
        keyword: Keyword search string. To be applied to any attributes that make sense
                    (as opposed to not making sense).
        min_price: Minimum price filter
        max_price: Maximum price filter
        free: Free items only flag. Sets min_price,max_price = 0
    route: /postquery/
    '''
    if settings.MOST_RECENT_CLEANUP != datetime.date.today():
        run_clean_up()
    json_data = {}
    
    try:
        #parse request
        request_data = ast.literal_eval(request.body)
        
        #get filter parameters from request
        keyword = request_data['keywordSearch']
        categories = request_data['categories']
        max_price = request_data['max_price'] #in case of nothing specified max_price will be empty string
        min_price = request_data['min_price'] #in case of nothing specified min_price will be empty string
        free = request_data['free']
        older = request_data['older']
        divider = request_data['divider_date_time']
        divider = divider.replace("\/","/")
        
        
        #get oldest post as datetime object
        #if none provided (base case) then set oldest_date to now plus two hours (just to be safe...)
        if not divider:
            divider_post_datetime = datetime.datetime.now(pytz.timezone('US/Pacific')) + datetime.timedelta(hours=2)
        
        #else use provided datetime
        else:
            divider_post_datetime = datetime.datetime.strptime(divider,'%m/%d/%Y %H:%M:%S')
        
                
        
        #clean keyword input
        keyword.strip() #removing leading or trailing whitespace
        keyword.replace("  "," ") #remove accidental double spaces
        
        #min_price and max_price not specified
        if not max_price:
            max_price = 10000.0
        else:
            max_price = float(max_price)
        if not min_price:           
            min_price = 0.0
        else:
            min_price = float(min_price)
        
        #react to free flag
        if free == "1":
            max_price = 0.0
            min_price = 0.0 
        
        print "keyword: " + str(keyword)
        print "categories: " + str(categories)
        print "max_price: " + str(max_price)
        print "min_price: " + str(min_price)
        print "free: " + str(free)
        print "divider_post_datetime: " + str(divider_post_datetime)
        print "older: " + str(older)
        
        
        
        def category_intersect(super_category,categories):
            '''
            Returns true if super_category and categories share an element
            '''
            for category1 in super_category:
                for category2 in categories:
                    if category1 == category2:
                        return True
        
        #set active categories---------------
        
        #in a populate as necessary sort of way...
        item_rs = None
        book_rs = None
        DL_rs = None
        RS_rs = None
        
        
        if older == "1":
            datetime_Q = Q(post_date_time__lt=divider_post_datetime)
            order_by_string = "-post_date_time"
            
        else:
            datetime_Q = Q(post_date_time__gt=divider_post_datetime)
            order_by_string = "post_date_time"
        
        
        #if no chosen category apply all
        if not categories:
            item_rs = ItemPost.objects.filter(datetime_Q,Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            book_rs = BookPost.objects.filter(datetime_Q,Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(isbn__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            DL_rs = DateLocationPost.objects.filter(datetime_Q,Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(location__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            RS_rs = RideSharePost.objects.filter(datetime_Q,Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(trip__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
        
        #category is of item type
        if category_intersect(item_categories,categories):
            #keyword applied to display_value, title, description
            item_rs = ItemPost.objects.filter(datetime_Q,Q(category__in=categories),Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            
        #category is of book type
        if category_intersect(book_categories,categories):
            #keyword applied to display_value, title, description, isbn
            book_rs = BookPost.objects.filter(datetime_Q,Q(category__in=categories),Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(isbn__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            
        #category is of book type
        if category_intersect(datelocation_categories,categories):
            #keyword applied to display_value, title, description, location
            DL_rs = DateLocationPost.objects.filter(datetime_Q,Q(category__in=categories),Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(location__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            
        #category is of book type
        if category_intersect(rideshare_categories,categories):
            #keyword applied to display_value, title, description, trip
            RS_rs = RideSharePost.objects.filter(datetime_Q,Q(category__in=categories),Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(trip__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            
        #populate the response with listview formatted results (grabs and encodes image data)
        json_data['posts'] = prepare_results(item_rs, book_rs, DL_rs, RS_rs, limit=settings.PAGING_COUNT)
        
        
        #hi five
        json_data['message'] = 'Successfully filtered and returned posts'
               
        #respond with json and 200 OK
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        
        return response
    
    #catch all unhandled exceptions
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
def run_clean_up():
    reported_posts = DateLocationPost.objects.filter(Q(report_count__gt=settings.MAX_REPORT_THRESHOLD))
    for post in reported_posts:
        remove_post(post)
        
    reported_posts = ItemPost.objects.filter(Q(report_count__gt=settings.MAX_REPORT_THRESHOLD))
    for post in reported_posts:
        remove_post(post)
   
    reported_posts = RideSharePost.objects.filter(Q(report_count__gt=settings.MAX_REPORT_THRESHOLD))
    for post in reported_posts:
        remove_post(post)  
    
    reported_posts = BookPost.objects.filter(Q(report_count__gt=settings.MAX_REPORT_THRESHOLD))
    for post in reported_posts:
        remove_post(post)  
        
    d1 = datetime.datetime.now(pytz.timezone('US/Pacific'))
    d2 = d1 - datetime.timedelta(days=settings.OLD_POST_CUTTOFF_LENGTH)
    
    old_posts = DateLocationPost.objects.filter(Q(post_date_time__lt=d2))
    for post in old_posts:
        remove_post(post)
        
    old_posts = RideSharePost.objects.filter(Q(post_date_time__lt=d2))
    for post in old_posts:
        remove_post(post)
        
    old_posts = ItemPost.objects.filter(Q(post_date_time__lt=d2))
    for post in old_posts:
        remove_post(post)
        
    old_posts = BookPost.objects.filter(Q(post_date_time__lt=d2))
    for post in old_posts:
        remove_post(post)
        
    settings.MOST_RECENT_CLEANUP = datetime.date.today()
    
        
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
        elif category in book_categories:
            post_info = BookPost.objects.get(id=post_id)
            json_data = view_book_post(request_data,json_data,post_info)
        elif category in datelocation_categories:
            post_info = DateLocationPost.objects.get(id=post_id)
            json_data = view_datelocation_post(request_data,json_data,post_info)
        elif category in rideshare_categories:
            post_info = RideSharePost.objects.get(id=post_id)
            json_data = view_rideshare_post(request_data,json_data,post_info)
        else:
            json_data['message'] =  'Error in viewing post: Invalid category'
            return HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
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
            if image_URLs_array[i] != settings.IMAGES_ROOT:
                image_file = open(image_URLs_array[i],"rb")
                image_data = image_file.read()
                images_base64_array[i] = encodestring(image_data)
                image_file.close()
      
        json_data["image1"] = images_base64_array[0]    
        json_data["image2"] = images_base64_array[1]    
        json_data["image3"] = images_base64_array[2]  
   
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
def view_book_post(request_data,json_data,Post):
    '''
    POST method for retrieving detailed Post data for book posts 
    (isbn)
    '''
    try:
        json_data["isbn"] = Post.isbn
        return json_data
    #general exception catching
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        return json_data

def view_rideshare_post(request_data,json_data,Post):
    '''
    POST method for retrieving detailed Post data for rideshare posts
    (roundtrip,trip,departure_date_time,return_date_time)
    '''
    try:
        json_data["trip"] = Post.trip
        hour = str((Post.departure_date_time.hour) % 12) #hour without leading zero
        if hour == "0": #weird attribute of time-keeping, 0 is actually 12
            hour = "12"
        minute_ampm = Post.departure_date_time.strftime(":%M%p") #minute and am/pm component
        json_data["departure_date_time"] = str(Post.departure_date_time.month) + "/" + str(Post.departure_date_time.day) + "/" + str(Post.departure_date_time.year)
        json_data["departure_date_time"] = json_data["departure_date_time"] + " " + hour + minute_ampm
        json_data["departure_date_time"] = str(Post.departure_date_time)
        if Post.round_trip:
            hour = str((Post.return_date_time.hour) % 12) #hour without leading zero
            if hour == "0": #weird attribute of time-keeping, 0 is actually 12
                hour = "12"
            minute_ampm = Post.return_date_time.strftime(":%M%p") #minute and am/pm component
            json_data["return_date_time"] = str(Post.return_date_time.month) + "/" + str(Post.return_date_time.day) + "/" + str(Post.return_date_time.year)
            json_data["return_date_time"] = json_data["return_date_time"] + " " + hour + minute_ampm
            json_data["return_date_time"] = str(Post.return_date_time)
            json_data["round_trip"] = 1
        else:
            json_data["round_trip"] = 0
        return json_data
    #general exception catching
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        return json_data

def view_datelocation_post(request_data,json_data,Post):
    '''
    POST method for retrieving detailed Post data for rideshare posts
    (date_time,location)
    '''
    try:
        hour = str((Post.date_time.hour) % 12) #hour without leading zero
        if hour == "0": #weird attribute of time-keeping, 0 is actually 12
            hour = "12"
        minute_ampm = Post.date_time.strftime(":%M%p") #minute and am/pm component
        json_data["date_time"] = str(Post.date_time.month) + "/" + str(Post.date_time.day) + "/" + str(Post.date_time.year)
        json_data["date_time"] = json_data["date_time"] + " " + hour + minute_ampm
        json_data["location"] = Post.location
        return json_data
    #general exception catching
    except Exception,e:
        print str(e)
        json_data['message'] = str(e)
        return json_data

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
        if category in item_categories: 
            return create_item_post(request_data,json_data)
        elif category in book_categories:
            return create_book_post(request_data,json_data)
        elif category in datelocation_categories:
            return create_datelocation_post(request_data,json_data)
        elif category in rideshare_categories:
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
            round_trip = int(request_data['round_trip']),
            gonzaga_email= int(request_data['gonzaga_email']),
            pref_email=int(request_data['pref_email']),
            call=int(request_data['call']),
            text=int(request_data['text']),
            display_value = trip_details,
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
    now = datetime.datetime.now(pytz.timezone('US/Pacific'))
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
        
@api_view(["post"])
def refresh_post(request):
    '''
    POST method for refreshing an existing post by bringing post_date_time to
    time of refresh. This represents the post bumping mechanism.
    Request body must contain the following data in JSON format:
        category: Category filter, member of collection of lowest level categories
        post_id: ID of a post in given category
    route: /refreshpost/
    '''
    json_data = {}
    try:
        request_data = ast.literal_eval(request.body) #parse request body
        
        #post keys
        post_id = request_data['post_id']
        post_category = request_data['category']

        #initially post is of type None, should remain None if not found
        post = None        

        #search the appropriate table, determined by category
        if post_category in item_categories:
            post = ItemPost.objects.get(id=post_id)
        elif post_category in book_categories:
            post = BookPost.objects.get(id=post_id)
        elif post_category in rideshare_categories:
            post = RideSharePost.objects.get(id=post_id)
        elif post_category in datelocation_categories:
            post = DateLocationPost.objects.get(id=post_id)
        
        #category doesn't exist, respond with 400 BAD REQUEST
        else:
            json_data["message"] = 'Error in Refreshing post: Invalid category'
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            return response

        #post not found by ID, respond with 400 BAD REQUEST          
        if not post:
            error_message = "Post with post_id " + str(post_id) + "could not be found"
            print error_message
            json_data['message'] = error_message
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            return response
       
        #perform the refresh: set post_date_time to now
        now = datetime.datetime.now(pytz.timezone('US/Pacific'))
        post.post_date_time = now
        
        #save changes
        post.save()

        #respond with HTTP 200 OK
        message = "Successfully refreshed " + post_category + " post with ID " + str(post_id)
        print message
        json_data['message'] = message
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        return response        
        
    #general exception handling
    except Exception, e:
        print str(e)
        json_data["message"] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
@api_view(['POST'])
def report_post(request):
    '''
    POST method for reporting an existing post by incrementing its report_count.
    Request body must contain the following data in JSON format:
        category: Category filter, member of collection of lowest level categories
        post_id: ID of a post in given category
    route: /reportpost/
    '''
    json_data = {}
    try:
        request_data = ast.literal_eval(request.body) #parse request body
        
        #post keys
        post_id = request_data['post_id']
        post_category = request_data['category']
        reporter = request_data['reporter']

        #check to see that the reporter hasn't already reported this post
        existing_report = PostReport.objects.filter(post_id=post_id,category=post_category,username_id=reporter)

        #if reporter has already hit this post, respond 200 with notification
        if existing_report:
            #respond with HTTP 200 OK
            message = "User " + reporter + " has already reported post " + str(post_id) + " in " + post_category
            print message
            json_data['message'] = message
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
            return response
        
        #if this report has yet to be made (existing_report == None) then create the report
        PostReport.objects.create(post_id=post_id,category=post_category,username_id=reporter)

        #initially post is of type None, should remain None if not found
        post = None        

        #search the appropriate table, determined by category
        if post_category in item_categories:
            post = ItemPost.objects.get(id=post_id)
        elif post_category in book_categories:
            post = BookPost.objects.get(id=post_id)
        elif post_category in rideshare_categories:
            post = RideSharePost.objects.get(id=post_id)
        elif post_category in datelocation_categories:
            post = DateLocationPost.objects.get(id=post_id)
        
        #category doesn't exist, respond with 400 BAD REQUEST
        else:
            error_message = "Non existent category: " + post_category
            print error_message
            json_data['message'] = error_message
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            return response
        
        #post not found by ID, respond with 400 BAD REQUEST          
        if not post:
            error_message = "Post with post_id " + str(post_id) + "could not be found"
            print error_message
            json_data['message'] = error_message
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            return response        
        
        #perform the report: increment post's report count
        current_count = post.report_count
        post.report_count = current_count + 1
        
        #save changes
        post.save()

        #respond with HTTP 200 OK
        message = "Successfully reported " + post_category + " post with ID " + str(post_id)
        print message
        json_data['message'] = message
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        return response        
        
    #general exception handling
    except Exception, e:
        print str(e)
        json_data["message"] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response