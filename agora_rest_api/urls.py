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
    (r'^ldapauth/','agora_rest_api.user_service.views.ldap_authenticate'),
    (r'^createuser/','agora_rest_api.user_service.views.create_user'),
    (r'^userprofile/','agora_rest_api.user_service.views.view_user'),
    (r'^edituser/','agora_rest_api.user_service.views.edit_user'),
)

