from django.conf.urls import patterns, include, url
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),

    '''User service urls'''
    #Url used for authenticating someone logging in and determining if they are a new user
    (r'^ldapauth/','agora_rest_api.user_service.views.ldap_authenticate'),
    #Url used to create a new user
    (r'^createuser/','agora_rest_api.user_service.views.create_user'),
    #Url used to view user information
    (r'^userprofile/','agora_rest_api.user_service.views.view_user'),
    #Url used to edit user information
    (r'^edituser/','agora_rest_api.user_service.views.edit_user'),
    #Url used to view all user posts
    (r'^userposts/','agora_rest_api.user_service.views.user_posts'),

    '''Post service urls'''
    #Url used to create a new post
    (r'^createpost/','agora_rest_api.post_service.create_post_views.create_post'),
    #Url used to view post information
    (r'^viewpost/','agora_rest_api.post_service.views.view_detailed_post'),
    #Url used to edit post information
    (r'^editpost/','agora_rest_api.post_service.edit_post_views.edit_post'),
    #Url used to mark a post as deleted
    (r'^deletepost/','agora_rest_api.post_service.views.delete_post'),
    #Url used to gather a list of posts and information
    (r'^postquery/','agora_rest_api.post_service.post_list_views.filter_post_list'),
    #Url used to refresh the post_date_time of a post
    (r'^refreshpost/','agora_rest_api.post_service.views.refresh_post'),
    #Url used to report a post
    (r'^reportpost/','agora_rest_api.post_service.views.report_post'),
    #Url used to get an image for a post
    (r'^getimage/','agora_rest_api.post_service.image_views.get_image'),
)

