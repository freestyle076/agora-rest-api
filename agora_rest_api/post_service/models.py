from django.db import models


class Post(models.Model):
    '''
    Post schema class model. Holds information on the Post and the post creater's 
    contact information.
    '''
    postid = models.CharField(max_length=40,unique=True)
    username = models.ForeignKey('user_service.User')
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    gonzaga_email = models.EmailField(null=True,blank=True)
    pref_email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=11,null=True,blank=True)
    price = models.CharField(max_length=10)

