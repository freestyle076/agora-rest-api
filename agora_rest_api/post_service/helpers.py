from agora_rest_api.post_service.models import BookPost, DateLocationPost, ItemPost, RideSharePost
from agora_rest_api.user_service.models import User, Analytics
from django.db.models import Q
from agora_rest_api import settings
import datetime
import pytz

# -*- coding: utf-8 -*-
"""
Table of Contents:
    category_intersect(super_category,categories)
    delete_imagefile(filename)
    remove_post(delete_post)
    run_clean_up()
"""

def category_intersect(super_category,categories):
    '''
    Returns true if super_category and categories share an element
    '''
    for category1 in super_category:
        for category2 in categories:
            if category1 == category2:
                return True
     

def remove_post(delete_post):
    '''
    Delete post function that doesn't Actually delete a post, 
    just marks it as deleted
    '''    
    json_data = {}
    json_data["message"] = ""
    #Assigns boolean variable to mark post as deleted
    try:
        delete_post.deleted = True
        delete_post.save()        
        return json_data["message"]
    except Exception,e:
        print str(e)
        json_data["message"] = str(e) 
        return json_data["message"]

"""    
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
"""
    
def run_clean_up():
    reported_posts = DateLocationPost.objects.filter(Q(report_count__gt=settings.MAX_REPORT_THRESHOLD)).exclude(deleted=1)
    analytic = Analytics.objects.get(id=1)
    #Gathers and deletes all posts that have been reported max number of times or more
    for post in reported_posts:
        del_user = User.objects.get(username=post.username_id)
        del_user.recent_post_deletion = 1
        del_user.save()
        #Increment number of deleted reported posts
        analytic.num_deleted_reported_posts = analytic.num_deleted_reported_posts + 1 
        analytic.save()
        remove_post(post)
              
    reported_posts = ItemPost.objects.filter(Q(report_count__gt=settings.MAX_REPORT_THRESHOLD)).exclude(deleted=1)
    for post in reported_posts:
        del_user = User.objects.get(username=post.username_id)
        del_user.recent_post_deletion = 1
        del_user.save()
        #Increment number of deleted reported posts
        analytic.num_deleted_reported_posts = analytic.num_deleted_reported_posts + 1 
        analytic.save()
        remove_post(post)
        
    reported_posts = RideSharePost.objects.filter(Q(report_count__gt=settings.MAX_REPORT_THRESHOLD)).exclude(deleted=1)
    for post in reported_posts:
        del_user = User.objects.get(username=post.username_id)
        del_user.recent_post_deletion = 1
        del_user.save()
        #Increment number of deleted reported posts
        analytic.num_deleted_reported_posts = analytic.num_deleted_reported_posts + 1 
        analytic.save()
        remove_post(post)
    
    reported_posts = BookPost.objects.filter(Q(report_count__gt=settings.MAX_REPORT_THRESHOLD)).exclude(deleted=1)
    for post in reported_posts:
        del_user = User.objects.get(username=post.username_id)
        del_user.recent_post_deletion = 1
        del_user.save()
        #Increment number of deleted reported posts
        analytic.num_deleted_reported_posts = analytic.num_deleted_reported_posts + 1 
        analytic.save()
        remove_post(post) 
        
    d1 = datetime.datetime.now(pytz.timezone(settings.TIME_ZONE))
    d2 = d1 - datetime.timedelta(days=settings.OLD_POST_CUTTOFF_LENGTH)
    
    #Gathers and deletes all posts that have are older than our cutoff length of time
    old_posts = DateLocationPost.objects.filter(Q(post_date_time__lt=d2)).exclude(deleted=1)
    for post in old_posts:
        del_user = User.objects.get(username=post.username_id)
        del_user.recent_post_deletion = 1
        del_user.save()
        remove_post(post)
        
    old_posts = RideSharePost.objects.filter(Q(post_date_time__lt=d2)).exclude(deleted=1)
    for post in old_posts:
        del_user = User.objects.get(username=post.username_id)
        del_user.recent_post_deletion = 1
        del_user.save()
        remove_post(post)
        
    old_posts = ItemPost.objects.filter(Q(post_date_time__lt=d2)).exclude(deleted=1)
    for post in old_posts:
        del_user = User.objects.get(username=post.username_id)
        del_user.recent_post_deletion = 1
        del_user.save()
        remove_post(post)
        
    old_posts = BookPost.objects.filter(Q(post_date_time__lt=d2)).exclude(deleted=1)
    for post in old_posts:
        del_user = User.objects.get(username=post.username_id)
        del_user.recent_post_deletion = 1
        del_user.save()
        remove_post(post)
        
    #Reassigns day of most recent cleanup to today    
    settings.MOST_RECENT_CLEANUP = datetime.date.today()
    
        
        
