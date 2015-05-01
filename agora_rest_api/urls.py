from django.conf.urls import patterns, include, url
from rest_framework import routers
import agora_rest_api

router = routers.DefaultRouter()

urlpatterns = patterns('',
    url(r'^', include(router.urls)),

    (r'^ldapauth/','agora_rest_api.user_service.views.ldap_authenticate'),
    (r'^createuser/','agora_rest_api.user_service.views.create_user'),
    (r'^userprofile/','agora_rest_api.user_service.views.view_user'),
    (r'^edituser/','agora_rest_api.user_service.views.edit_user'),
    (r'^userposts/','agora_rest_api.user_service.views.user_posts'),
    (r'^stats/','agora_rest_api.user_service.views.stats'),

    (r'^createpost/','agora_rest_api.post_service.create_post_views.create_post'),
    (r'^viewpost/','agora_rest_api.post_service.views.view_detailed_post'),
    (r'^editpost/','agora_rest_api.post_service.edit_post_views.edit_post'),
    (r'^deletepost/','agora_rest_api.post_service.views.delete_post'),
    (r'^postquery/','agora_rest_api.post_service.post_list_views.filter_post_list'),
    (r'^refreshpost/','agora_rest_api.post_service.views.refresh_post'),
    (r'^reportpost/','agora_rest_api.post_service.views.report_post'),
    (r'^getimage/','agora_rest_api.post_service.image_views.get_image'),
)

