from django.conf.urls import patterns, include, url
from rest_framework import routers
from user_service import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agora_rest_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),

    #user service
    (r'^ldapauth/','agora_rest_api.user_service.views.ldap_authenticate'),
    (r'^createuser/','agora_rest_api.user_service.views.create_user'),
    (r'^userprofile/','agora_rest_api.user_service.views.view_user'),
    (r'^edituser/','agora_rest_api.user_service.views.edit_user'),
    (r'^userposts/','agora_rest_api.user_service.views.user_posts'),

    #post service
    (r'^createpost/','agora_rest_api.post_service.views.create_post'),
    (r'^viewpost/','agora_rest_api.post_service.views.view_detailed_post'),
    (r'^editpost/','agora_rest_api.post_service.views.edit_post'),
    (r'^postquery/','agora_rest_api.post_service.views.filter_post_list'),
    
)

