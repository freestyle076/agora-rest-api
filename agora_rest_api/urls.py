from django.conf.urls import patterns, include, url
from rest_framework import routers
#from user_service import views

router = routers.DefaultRouter()
<<<<<<< HEAD
router.register(r'users', views.UserViewSet)
router.register(r'ldap', views.ldapViewSet)
=======
#router.register(r'users', views.UserViewSet)
>>>>>>> 2824223e4db6ffe319926745aa09fcf78a393187

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agora_rest_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^', include(router.urls)),
    (r'^ldapauth/$','agora_rest_api.user_service.views.ldap_authenticate'),
)

