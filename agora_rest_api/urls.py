from django.conf.urls import patterns, include, url
from rest_framework import routers
from user_service import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'agora_rest_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
)
