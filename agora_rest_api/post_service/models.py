from django.db import models
import datetime

class ListPost(models.Model):
    '''
    Class for storing data on our post and displaying in List Format
    '''
    display_value = models.CharField(max_length=40,default='')
    postid = models.CharField(max_length=40,unique=True,default=1)
    title = models.CharField(max_length=50,default='')
    category = models.CharField(max_length=20,default='')
    postDateTime = models.DateTimeField(default=datetime.date.today())
    
    class Meta:
        abstract = True
    
class Post(ListPost):
    '''
    General Post Schema,
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    gonzaga_email = models.EmailField(null=True)
    pref_email = models.EmailField(null=True)
    phone = models.CharField(max_length=11,null=True)
    price = models.CharField(max_length=10,default='')
    class Meta:
        abstract = True

class ItemPost(Post):
    '''
    Items works for our item categories
    Electronics, furniture, appliances/kitchen, and recreation
    '''
    username = models.ForeignKey('user_service.User')
    
class BookPost(Post):
    '''
    Class for Books, additional Attribute is ISBN
    '''
    isbn = models.CharField(max_length=12,default='')
    username = models.ForeignKey('user_service.User')
    
class DateLocationPost(Post):
    '''
    Class for categories that require a date and time
    Events, Services
    '''
    date_time = models.DateTimeField(default=datetime.date.today())
    location = models.CharField(max_length=20)
    username = models.ForeignKey('user_service.User')
    
class RideSharePost(Post):
    '''
    Class for RideShare Posts, additional attributes are trip details and 
    a bool signifying if it is a round trip or not.
    return_date_time only needed if it is a round trip
    '''
    start_date_time = models.DateTimeField(default=datetime.date.today())
    return_date_time = models.DateTimeField(default=datetime.date.today())
    trip = models.CharField(max_length=50,default='')
    round_trip = models.BooleanField(default=True)
    username = models.ForeignKey('user_service.User')
