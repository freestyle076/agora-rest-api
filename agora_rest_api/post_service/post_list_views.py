from rest_framework import status
from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost
from agora_rest_api.post_service import helpers
from agora_rest_api import settings
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.db.models import Q
import datetime
import json
import ast
import pytz


# -*- coding: utf-8 -*-

"""
Table of Contents:
    user_posts(username)
    prepare_results(items, books, DLs, RSs, limit=0)
    filter_post_list(request)
"""

time_zone_loc = pytz.timezone(settings.TIME_ZONE)
time_zone_utc = pytz.timezone('UTC')

def user_posts(username,divider,older):
    '''
    Gathers an aggregate list of posts, in listview format, that belong to
    the user whose username matches parameter username
    username: user whose posts will be collected
    divider: date time divider specifying where to resume loading posts
    older: flag signifying post return direction. 
        1: posts older than divider chronologically
        0: posts younger than divider chronologically
    '''
    
    
    try:
    
        #get oldest post as datetime object
        #if none provided (base case) then set oldest_date to now plus two hours (just to be safe...)
        if not divider:
            divider_post_datetime = datetime.datetime.now(pytz.timezone('UTC')) + datetime.timedelta(hours=2)

        
        #else use provided datetime
        else:
            divider_post_datetime = time_zone_utc.localize(datetime.datetime.strptime(divider,'%m/%d/%Y %H:%M:%S'))        
        
        
        #alter database queries according 
        #older means post_date_time less than divider in descending order
        if older == "1":
            datetime_Q = Q(post_date_time__lt=divider_post_datetime)
            order_by_string = "-post_date_time"
            edge_index = -1
        #newer (not older) means post_date_time greater than divider in ascending order
        else:
            datetime_Q = Q(post_date_time__gt=divider_post_datetime)
            order_by_string = "post_date_time"
            edge_index = 0
            
        #collect posts belonging to the user
        item_rs = ItemPost.objects.filter(Q(deleted__exact=False),datetime_Q,Q(username_id__exact=username)).order_by(order_by_string)[:settings.PAGING_COUNT]
        book_rs = BookPost.objects.filter(Q(deleted__exact=False),datetime_Q,Q(username_id__exact=username)).order_by(order_by_string)[:settings.PAGING_COUNT]
        DL_rs = DateLocationPost.objects.filter(Q(deleted__exact=False),datetime_Q,Q(username_id__exact=username)).order_by(order_by_string)[:settings.PAGING_COUNT]
        RS_rs = RideSharePost.objects.filter(Q(deleted__exact=False),datetime_Q,Q(username_id__exact=username)).order_by(order_by_string)[:settings.PAGING_COUNT]
        
        #prepare the results: listview format in order of post date
        posts = prepare_results(item_rs,book_rs,DL_rs,RS_rs,limit=settings.PAGING_COUNT)
        
        def more_to_gather(older,edge_post):
            '''
            Checks if there are more posts in the older or newer direction as specified 
            by the older variable. Returns true if there are more, false if there are not.
            '''
            
            #form edge date_time string into date_time object
            edge_date_time = time_zone_utc.localize(datetime.datetime.strptime(edge_post['post_date_time'],'%m/%d/%Y %H:%M:%S'))   
            
            #assign query parameter according to function parameter 'older'
            if older == "1":
                date_time_compare_Q = Q(post_date_time__lt=edge_date_time)
            else:
                date_time_compare_Q = Q(post_date_time__gt=edge_date_time)

            #default exist variables to False for each table
            items_exist = False
            books_exist = False           
            RSs_exist = False           
            DLs_exist = False           

            
            #more item posts?
            items_exist = ItemPost.objects.filter(date_time_compare_Q,Q(username_id__exact=username)).exists()
            
            #more book posts?
            books_exist = BookPost.objects.filter(date_time_compare_Q,Q(username_id__exact=username)).exists()
            
            #more RS posts?
            RSs_exist = RideSharePost.objects.filter(date_time_compare_Q,Q(username_id__exact=username)).exists()
                
            #more DL posts?
            DLs_exist = DateLocationPost.objects.filter(date_time_compare_Q,Q(username_id__exact=username)).exists()
            
            #check if any more posts in ANY TABLE exist in the direction specified by 'older'
            more_exist =  items_exist or books_exist or RSs_exist or DLs_exist
            
             
            return more_exist
    
        #first check if there were results. If there weren't any then there
        #couldn't be any more...
        if posts:
            #if there are results then check to see if there are more results
            more_exist = str(int(more_to_gather(older,posts[edge_index])))
        else:
            more_exist = "0"
            
        
        return posts,more_exist
        
    #general exception handling
    except Exception, e:
        raise e
        

def prepare_results(items, books, DLs, RSs, limit=None):
    '''
    Prepares a list a filter request results, each in listview post format.
    Returns a list of objects, ready to be included in a JSON object.
    items: ItemPost resultset
    books: BookPost resultset
    DLs: DateLocationPost resultset
    RSs: RidesharePost resultset
    '''    
    
    posts = []
        
    try:
        #items
        if items:
            for item in items: #iterate through each post
                if item.image1: #check for default image
                    has_image = True
                else:
                    has_image = False
                
                #switch on price value
                if item.price == None:
                    display_value_temp = '' #null is empty string
                elif float(item.price) == 0.: 
                    display_value_temp = 'Free' #zero is free
                else:
                    display_value_temp = "${:.2f}".format(float(item.price))
                    
                #format and append to posts list
                listview_item = {'has_image':has_image,'id':item.id,'title':item.title,'category':item.category,'display_value':display_value_temp,'post_date_time':item.post_date_time.strftime('%m/%d/%Y %H:%M:%S')}
                posts.append(listview_item)
                
                
        #books
        if books:
            for book in books: #iterate through each post
                if book.image1: #check for default image
                    has_image = True
                else:
                    has_image = False

                if book.price == None:
                    display_value_temp = '' #null is empty string
                elif float(book.price) == 0.:
                    display_value_temp = 'Free' #zero is free
                else:
                    display_value_temp = "${:.2f}".format(float(book.price))                    
                    
                #format and append to posts list
                listview_book = {'has_image':has_image,'id':book.id,'title':book.title,'category':book.category,'display_value':display_value_temp,'post_date_time':book.post_date_time.strftime('%m/%d/%Y %H:%M:%S')}
                posts.append(listview_book)


        #Datelocations
        if DLs:
            for DL in DLs: #iterate through each post
                if DL.image1: #check for default image
                    has_image = True
                else:
                    has_image = False
                if DL.date_time:
                    month = str(DL.date_time.month) #month without leading zero
                    hour = str((DL.date_time.hour) % 12) #hour without leading zero
                    day = str(DL.date_time.day)
                    if hour == "0": #weird attribute of time-keeping, 0 is actually 12
                        hour = "12"
                        year = DL.date_time.strftime("%y") #day and year component
                        minute_ampm = DL.date_time.strftime(":%M%p") #minute and am/pm component
                
                    display_value_temp = month + "/" + day + "/" + year + " " + hour + minute_ampm
                else:
                    if DL.price == None:
                        display_value_temp = '' #null is empty string
                    elif float(DL.price) == 0.:
                        display_value_temp = 'Free' #zero is free
                    else:
                        display_value_temp = "${:.2f}".format(float(DL.price))
                
                #format and append to posts list
                listview_DL = {'has_image':has_image,'id':DL.id,'title':DL.title,'category':DL.category,'display_value':display_value_temp,'post_date_time':DL.post_date_time.strftime('%m/%d/%Y %H:%M:%S'),}
                posts.append(listview_DL)


        #Rideshares
        if RSs:
            for RS in RSs: #iterate through each post
                if RS.image1: #check for default image
                    has_image = True
                else:
                    has_image = False
                
                if RS.price == None:
                    display_value_temp = '' #null is empty string
                elif float(RS.price) == 0.:
                    display_value_temp = 'Free' #zero is free
                else:
                    display_value_temp = "${:.2f}".format(float(RS.price)) 
                    
                #format and append to posts list
                listview_RS = {'has_image':has_image,'id':RS.id,'title':RS.title,'category':RS.category,'display_value':display_value_temp,'post_date_time':RS.post_date_time.strftime('%m/%d/%Y %H:%M:%S')}
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
        
        #if a limit is provided then take 0 ~ limit - 1
        if limit:
            posts = posts[:limit]
                
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
    
    #if this is the first time the filter_post_list function has been called
    #on this day then run the cleanup function
    if settings.MOST_RECENT_CLEANUP != datetime.date.today():
        helpers.run_clean_up()
        
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
        
        
        #quick little cover up...
        if 'Rideshares' in categories:
            categories.append("Ride Shares")
        
        #get oldest post as datetime object
        #if none provided (base case) then set oldest_date to now plus two hours (just to be safe...)
        if not divider:
            divider_post_datetime = datetime.datetime.now(pytz.timezone('UTC')) + datetime.timedelta(hours=2)

        
        #else use provided datetime
        else:
            divider_post_datetime = time_zone_utc.localize(datetime.datetime.strptime(divider,'%m/%d/%Y %H:%M:%S'))
        
                
        #clean keyword input
        keyword.strip() #removing leading or trailing whitespace
        keyword.replace("  "," ") #remove accidental double spaces
        
        
        #establish queries for max_price and min_price
        allow_nulls = True
        #if no max price set to upper bound
        if not max_price:
            max_price = 10000.0
        #else set to given max_price and no nulls
        else:
            max_price = float(max_price)
            allow_nulls = False
        #if no min_price set to lower bound
        if not min_price:   
            min_price = 0.0
        #else set to given min_price and no nulls
        else:
            min_price = float(min_price)
            allow_nulls = False
        
        #react to free flag
        if free == "1":
            max_price = 0.0
            min_price = 0.0 
            allow_nulls = False
        
        #if nulls are allowed include in price Qs
        if allow_nulls:
            
            max_price_Q = Q(price__lte=max_price) | Q(price__isnull=True)
            min_price_Q = Q(price__gte=min_price) | Q(price__isnull=True)
        #else don't include nulls in price Qs
        else:
            max_price_Q = Q(price__lte=max_price)
            min_price_Q = Q(price__gte=min_price)    
        
        
        #set active categories---------------
        
        #in a populate as necessary sort of way...
        item_rs = None
        book_rs = None
        DL_rs = None
        RS_rs = None
        
        #alter database queries according 
        #older means post_date_time less than divider in descending order
        if older == "1":
            datetime_Q = Q(post_date_time__lt=divider_post_datetime)
            order_by_string = "-post_date_time"
            edge_index = -1
        #newer (not older) means post_date_time greater than divider in ascending order
        else:
            datetime_Q = Q(post_date_time__gt=divider_post_datetime)
            order_by_string = "post_date_time"
            edge_index = 0
        
        
        #if no chosen category apply all
        if not categories:
            categories = settings.item_categories + settings.book_categories + settings.datelocation_categories + settings.rideshare_categories
        
        #category is of item type
        if helpers.category_intersect(settings.item_categories,categories):
            #keyword applied to display_value, title, description
            item_rs = ItemPost.objects.filter(Q(deleted__exact=False),datetime_Q,Q(category__in=categories),max_price_Q,min_price_Q,Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            
        #category is of book type
        if helpers.category_intersect(settings.book_categories,categories):
            #keyword applied to display_value, title, description, isbn
            book_rs = BookPost.objects.filter(Q(deleted__exact=False),datetime_Q,Q(category__in=categories),max_price_Q,min_price_Q,Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(isbn__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            
        #category is of datelocation type
        if helpers.category_intersect(settings.datelocation_categories,categories):
            #keyword applied to display_value, title, description, location
            DL_rs = DateLocationPost.objects.filter(Q(deleted__exact=False),datetime_Q,Q(category__in=categories),max_price_Q,min_price_Q,Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(location__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            
        #category is of rideshares type
        if helpers.category_intersect(settings.rideshare_categories,categories):
            #keyword applied to display_value, title, description, trip
            RS_rs = RideSharePost.objects.filter(Q(deleted__exact=False),datetime_Q,Q(category__in=categories),max_price_Q,min_price_Q,Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(trip__icontains=keyword)).order_by(order_by_string)[:settings.PAGING_COUNT]
            
        #populate the response with listview formatted results (grabs and encodes image data)
        results = prepare_results(item_rs, book_rs, DL_rs, RS_rs, limit=settings.PAGING_COUNT)
        json_data['posts'] = results
        
        
        def more_to_gather(older,edge_post):
            '''
            Checks if there are more posts in the older or newer direction as specified 
            by the older variable. Returns true if there are more, false if there are not.
            '''
            
            #form edge date_time string into date_time object
            edge_date_time = time_zone_utc.localize(datetime.datetime.strptime(edge_post['post_date_time'],'%m/%d/%Y %H:%M:%S'))   
            
            #assign query parameter according to function parameter 'older'
            if older == "1":
                date_time_compare_Q = Q(post_date_time__lt=edge_date_time)
            else:
                date_time_compare_Q = Q(post_date_time__gt=edge_date_time)

            #default exist variables to False for each table
            items_exist = False
            books_exist = False           
            RSs_exist = False           
            DLs_exist = False           

            
            #more item posts?
            if helpers.category_intersect(settings.item_categories,categories):
                items_exist = ItemPost.objects.filter(date_time_compare_Q,Q(category__in=categories),Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword)).exists()
            
            #more book posts?
            if helpers.category_intersect(settings.book_categories,categories):
                books_exist = BookPost.objects.filter(date_time_compare_Q,Q(category__in=categories),Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(isbn__icontains=keyword)).exists()
            
            #more RS posts?
            if helpers.category_intersect(settings.rideshare_categories,categories):
                RSs_exist = RideSharePost.objects.filter(date_time_compare_Q,Q(category__in=categories),Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(trip__icontains=keyword)).exists()
                
            #more DL posts?
            if helpers.category_intersect(settings.datelocation_categories,categories):
                DLs_exist = DateLocationPost.objects.filter(date_time_compare_Q,Q(category__in=categories),Q(price__lte=max_price),Q(price__gte=min_price),Q(display_value__icontains=keyword) | Q(title__icontains=keyword)  | Q(description__icontains=keyword) | Q(location__icontains=keyword)).exists()
            
            #check if any more posts in ANY TABLE exist in the direction specified by 'older'
            more_exist =  items_exist or books_exist or RSs_exist or DLs_exist
            
             
            return more_exist
            
        #first check if there were results. If there weren't any then there
        #couldn't be any more...
        if results:
            #if there are results then check to see if there are more results
            more_exist = str(int(more_to_gather(older,results[edge_index])))
        else:
            #else there are no more results
            more_exist = "0"
            
        json_data['more_exist'] = more_exist
        
        #hi five
        json_data['message'] = 'Successfully filtered and returned posts'
               
        #respond with json and 200 OK
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        
        return response
    
    #catch all unhandled exceptions
    except Exception,e:
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response