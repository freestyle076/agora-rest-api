from django.db import models
import datetime

class ListPost(models.Model):
    '''
    Class for storing data on our post and displaying in List Format
    '''
    display_value = models.CharField(max_length=40)
    post_id = models.CharField(max_length=40,unique=True)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    post_date_time = models.DateTimeField(default=datetime.datetime.now())
    image1 = models.CharField(max_length=26,blank=True)
    
    
    class Meta:
        abstract = True

class ItemPost(ListPost):
    '''
    Items works for our item categories
    Electronics, furniture, appliances/kitchen, and recreation
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    gonzaga_email = models.EmailField(null=True)
    pref_email = models.EmailField(null=True)
    phone = models.CharField(max_length=11,null=True)
    price = models.PositiveIntegerField()
    username = models.ForeignKey('user_service.User')
    image2 = models.CharField(max_length=26,blank=True)
    image3 = models.CharField(max_length=26,blank=True)  
    
class BookPost(ListPost):
    '''
    Class for Books, additional Attribute is ISBN
    '''
    isbn = models.CharField(max_length=12)
    description = models.CharField(max_length=1000,blank=True)
    gonzaga_email = models.EmailField(null=True)
    pref_email = models.EmailField(null=True)
    phone = models.CharField(max_length=11,null=True)
    price = models.PositiveIntegerField()
    username = models.ForeignKey('user_service.User')
    image2 = models.CharField(max_length=26,blank=True)
    image3 = models.CharField(max_length=26,blank=True)  
    
class DateLocationPost(ListPost):
    '''
    Class for categories that require a date and time
    Events, Services
    '''
    date_time = models.DateTimeField(default=datetime.date.today())
    location = models.CharField(max_length=20)
    description = models.CharField(max_length=1000,blank=True)
    gonzaga_email = models.EmailField(null=True)
    pref_email = models.EmailField(null=True)
    phone = models.CharField(max_length=11,null=True)
    price = models.PositiveIntegerField()
    username = models.ForeignKey('user_service.User')
    image2 = models.CharField(max_length=26,blank=True)
    image3 = models.CharField(max_length=26,blank=True)  
    
class RideSharePost(ListPost):
    '''
    Class for RideShare Posts, additional attributes are trip details and 
    a bool signifying if it is a round trip or not.
    return_date_time only needed if it is a round trip
    '''
    departure_date_time = models.DateTimeField(default=datetime.date.today())
    return_date_time = models.DateTimeField(default=datetime.date.today())
    trip = models.CharField(max_length=50)
    round_trip = models.BooleanField(default=False)
    
    description = models.CharField(max_length=1000,blank=True)
    gonzaga_email = models.EmailField(null=True)
    pref_email = models.EmailField(null=True)
    phone = models.CharField(max_length=11,null=True)
    price = models.PositiveIntegerField()
    username = models.ForeignKey('user_service.User')
    image2 = models.CharField(max_length=26,blank=True)
    image3 = models.CharField(max_length=26,blank=True)  
