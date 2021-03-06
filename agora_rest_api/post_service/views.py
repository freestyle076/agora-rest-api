from rest_framework import status
from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost, PostReport
from agora_rest_api.post_service import helpers
from agora_rest_api.user_service.models import User, Analytics
from agora_rest_api import settings
from rest_framework.decorators import api_view
from django.http import HttpResponse
import datetime
import json
import ast
import pytz

"""
Table of Contents:
    delete_post(request)
    view_detailed_post(request)
    view_book_post(request_data,json_data,Post)
    view_rideshare_post(request_data,json_data,Post)
    view_datelocation_post(request_data,json_data,Post)
    refresh_post(request)
    report_post(request)
"""


date_time_format = "%m\/%d\/%Y %I:%M %p"
time_zone_loc = pytz.timezone(settings.TIME_ZONE)
time_zone_utc = pytz.timezone('UTC')

        
@api_view(['POST'])
def delete_post(request):
    '''  
    POST method for deleting a Post and its images
    route: /deletepost/
    '''
    json_data = {}
    try:
        #parse data
        request_data = ast.literal_eval(request.body)
        
        #switch on post category
        category = request_data["category"]
        if category in settings.item_categories:
            delete_post = ItemPost.objects.get(id=request_data['id'])
        elif category in settings.book_categories:
            delete_post = BookPost.objects.get(id=request_data['id'])
        elif category in settings.datelocation_categories:
            delete_post = DateLocationPost.objects.get(id=request_data['id'])
        elif category in settings.rideshare_categories:
            delete_post = RideSharePost.objects.get(id=request_data['id'])
        #catch case in which category doesn't exist
        else:
            json_data = {'message': 'Error in Editing post: Invalid category'}
            return HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        
        #returned value from helpers.remove_post is either empty string or error
        json_data["message"] = helpers.remove_post(delete_post)
        
        #Increment number of Item posts in analytics
        analytic = Analytics.objects.get(id=1)
        analytic.num_manually_deleted_posts = analytic.num_manually_deleted_posts + 1 
        analytic.save()
        
        #if returned value from helpers.remove_post is empty then return success
        if json_data["message"] == "":
            json_data['message'] = "Succesfully Deleted Post"   
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
    
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
        #parse data
        request_data = ast.literal_eval(request.body)

        #get id of post        
        post_id = request_data['post_id']
        
        #switch on category        
        category = request_data['category'] 
        if category in settings.item_categories:
            post_info = ItemPost.objects.get(id=post_id)    
        elif category in settings.book_categories:
            post_info = BookPost.objects.get(id=post_id)
            json_data = view_book_post(request_data,json_data,post_info)
        elif category in settings.datelocation_categories:
            post_info = DateLocationPost.objects.get(id=post_id)
            json_data = view_datelocation_post(request_data,json_data,post_info)
        elif category in settings.rideshare_categories:
            post_info = RideSharePost.objects.get(id=post_id)
            json_data = view_rideshare_post(request_data,json_data,post_info)
        
        #catch case in which category doesn't exist
        else:
            json_data['message'] =  'Error in viewing post: Invalid category'
            return HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')

        #assign return values for title and username        
        json_data['title'] = post_info.title
        json_data['username'] = post_info.username_id        
        
        #get associated user object        
        post_user = User.objects.get(username=post_info.username_id)
        
        #formulate returned price value according to stored price value
        if post_info.price == None:
            price_temp = '' #null price is empty string
        elif float(post_info.price) == 0.:
            price_temp = 'Free' #zero is free
        else:
            price_temp = "${:.2f}".format(float(post_info.price))
                      
        #return formulated price value
        json_data['price'] = price_temp

        #return description             
        json_data['description'] = post_info.description
        
        #ensure that at least one contact option is allowed
        #if not, default to allowing Zagmail
        enoughContactOptions = False
        if post_info.call == 1:
            json_data["call"] = post_user.phone
            if json_data["call"] != '':
                enoughContactOptions = True
        else:
            json_data["call"] = ''
        if post_info.text == 1:
            json_data["text"] = post_user.phone
            if json_data["text"] != '':
                enoughContactOptions = True
        else:
            json_data["text"] = ''
        if post_info.pref_email == 1:
            json_data["pref_email"] = post_user.pref_email
            if json_data["pref_email"] != '':
                enoughContactOptions = True
        else:
            json_data["pref_email"] = ''
            
        if post_info.gonzaga_email == 1 or not enoughContactOptions:
            json_data["gonzaga_email"] = post_user.gonzaga_email
        else:
            json_data["gonzaga_email"] = ''
        
        #count up the images for image_count returned value
        image_count = 0
        if post_info.image1:
            image_count += 1
        if post_info.image2:
            image_count += 1
        if post_info.image3:
            image_count += 1
        json_data["image_count"] = image_count

        #Increment number of Item posts in analytics
        analytic = Analytics.objects.get(id=1)
        analytic.num_post_views = analytic.num_post_views + 1 
        analytic.save()
        
        return HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        
    #general exception catching
    except Exception,e:
        json_data['message'] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response
        
def view_book_post(request_data,json_data,Post):
    '''
    POST method for retrieving detailed Post data for book posts 
    (isbn)
    '''
    try:
        #additional isbn field
        json_data["isbn"] = Post.isbn
        return json_data
    #general exception catching
    except Exception,e:
        json_data['message'] = str(e)
        return json_data

def view_rideshare_post(request_data,json_data,Post):
    '''
    POST method for retrieving detailed Post data for rideshare posts
    (roundtrip,trip,departure_date_time,return_date_time)
    '''
    try:
        #additional trip field
        json_data["trip"] = Post.trip
        
        #if there is a departure_date_time then correctly format it 
        if Post.departure_date_time:
            hour = str((Post.departure_date_time.hour) % 12) #hour without leading zero
            if hour == "0": #weird attribute of time-keeping, 0 is actually 12
                hour = "12"
            minute_ampm = Post.departure_date_time.strftime(":%M %p") #minute and am/pm component
            year_short = Post.departure_date_time.strftime("%y") #short version of year (without century)
            json_data["departure_date_time"] = str(Post.departure_date_time.month) + "/" + str(Post.departure_date_time.day) + "/" + year_short + ","
            json_data["departure_date_time"] = json_data["departure_date_time"] + " " + hour + minute_ampm
        #else return empty string
        else:
            json_data["departure_date_time"] = ''
        
        #if the post is a round trip then handle return_date_time
        if Post.round_trip:
            #if there is a return_date_time then correctly format it 
            if Post.return_date_time:
                hour = str((Post.return_date_time.hour) % 12) #hour without leading zero
                if hour == "0": #weird attribute of time-keeping, 0 is actually 12
                    hour = "12"
                minute_ampm = Post.return_date_time.strftime(":%M %p") #minute and am/pm component
                year_short = Post.return_date_time.strftime("%y") #short version of year (without century)
                json_data["return_date_time"] = str(Post.return_date_time.month) + "/" + str(Post.return_date_time.day) + "/" + year_short + ","
                json_data["return_date_time"] = json_data["return_date_time"] + " " + hour + minute_ampm
            #else return empty string
            else:
                json_data["return_date_time"] = ''
            #return that the post is a round_trip
            json_data["round_trip"] = 1
        #else the post isn't a round trip
        else:
            json_data["round_trip"] = 0
        return json_data
        
    #general exception catching
    except Exception,e:
        json_data['message'] = str(e)
        return json_data

def view_datelocation_post(request_data,json_data,Post):
    '''
    POST method for retrieving detailed Post data for rideshare posts
    (date_time,location)
    '''
    try:
        #if there is a date_time then correctly format it
        if Post.date_time:
            hour = str((Post.date_time.hour) % 12) #hour without leading zero
            if hour == "0": #weird attribute of time-keeping, 0 is actually 12
                hour = "12"
            minute_ampm = Post.date_time.strftime(":%M %p") #minute and am/pm component
            short_year = Post.date_time.strftime("%y")
            json_data["date_time"] = str(Post.date_time.month) + "/" + str(Post.date_time.day) + "/" + short_year + ","
            json_data["date_time"] = json_data["date_time"] + " " + hour + minute_ampm
        #else return empty string
        else:
            json_data["date_time"] = ''
        json_data["location"] = Post.location
        return json_data
    #general exception catching
    except Exception,e:
        json_data['message'] = str(e)
        return json_data


@api_view(['POST'])
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
        if post_category in settings.item_categories:
            post = ItemPost.objects.get(id=post_id)
        elif post_category in settings.book_categories:
            post = BookPost.objects.get(id=post_id)
        elif post_category in settings.rideshare_categories:
            post = RideSharePost.objects.get(id=post_id)
        elif post_category in settings.datelocation_categories:
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
        
        #users can only refresh once a day, as tracked by post.last_refresh_date
        if post.last_refresh_date == datetime.date.today():
            message = post_category + " post with ID " + str(post_id) + " has already been refreshed today"
            print message
            json_data['message'] = message
            json_data['refreshed'] = '0'
            json_data['post_date_time'] = post.post_date_time.strftime('%m/%d/%Y %H:%M:%S')
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
            return response
        
        utc_now = time_zone_utc.localize(datetime.datetime.utcnow()) #get UTC now, timezone set to UTC
        now = time_zone_loc.normalize(utc_now) #normalize to local timezone
        
        #refresh the post's datetime        
        post.post_date_time = now
        
        #update the post's last_refresh_date
        post.last_refresh_date = datetime.date.today()
        
        #save changes
        post.save()

        #respond with HTTP 200 OK
        message = "Successfully refreshed " + post_category + " post with ID " + str(post_id)
        print message
        json_data['message'] = message
        json_data['refreshed'] = '1'
        json_data['post_date_time'] = post.post_date_time.strftime('%m/%d/%Y %H:%M:%S')
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        return response        
        
    #general exception handling
    except Exception, e:
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
            json_data['message'] = message
            json_data['reported'] = "0"
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
            return response
        
        #if this report has yet to be made (existing_report == None) then create the report
        PostReport.objects.create(post_id=post_id,category=post_category,username_id=reporter)

        #initially post is of type None, should remain None if not found
        post = None        

        #search the appropriate table, determined by category
        if post_category in settings.item_categories:
            post = ItemPost.objects.get(id=post_id)
        elif post_category in settings.book_categories:
            post = BookPost.objects.get(id=post_id)
        elif post_category in settings.rideshare_categories:
            post = RideSharePost.objects.get(id=post_id)
        elif post_category in settings.datelocation_categories:
            post = DateLocationPost.objects.get(id=post_id)
        
        #category doesn't exist, respond with 400 BAD REQUEST
        else:
            error_message = "Non existent category: " + post_category
            json_data['message'] = error_message
            response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
            return response
        
        #post not found by ID, respond with 400 BAD REQUEST          
        if not post:
            error_message = "Post with post_id " + str(post_id) + "could not be found"
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
        json_data['reported'] = "1"
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_200_OK,content_type='application/json')
        return response        
        
    #general exception handling
    except Exception, e:
        json_data["message"] = str(e)
        response = HttpResponse(json.dumps(json_data),status=status.HTTP_400_BAD_REQUEST,content_type='application/json')
        return response