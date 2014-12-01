from django.db import models
import datetime

class ListPost(models.Model):
    '''
    Class for storing data on our post and displaying in List Format
    '''
    display_value = models.CharField(max_length=40)
    title = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    post_date_time = models.DateTimeField()
    image1 = models.CharField(max_length=26,blank=True,default='') #url
    
    class Meta:
        abstract = True

class ItemPost(ListPost):
    '''
    Items works for our item categories
    Electronics, furniture, appliances/kitchen, and recreation
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.PositiveIntegerField()
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False)
    pref_email = models.BooleanField(default=False)
<<<<<<< HEAD
    call = models.BooleanField(default=False)
=======
    phone = models.BooleanField(default=False)
>>>>>>> 1746326dc8c92a96bbacac7aa8796cfb59565f18
    text = models.BooleanField(default=False)
    image2 = models.CharField(max_length=26,blank=True,default='') #url
    image3 = models.CharField(max_length=26,blank=True,default='') #url
    
class BookPost(ListPost):
    '''
    Class for Books, additional Attribute is ISBN
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.PositiveIntegerField()
    isbn = models.CharField(max_length=12)
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False)
    pref_email = models.BooleanField(default=False)
<<<<<<< HEAD
    call = models.BooleanField(default=False)
=======
    phone = models.BooleanField(default=False)
>>>>>>> 1746326dc8c92a96bbacac7aa8796cfb59565f18
    text = models.BooleanField(default=False)
    image2 = models.CharField(max_length=26,blank=True,default='') #url
    image3 = models.CharField(max_length=26,blank=True,default='') #url

    
class DateLocationPost(ListPost):
    '''
    Class for categories that require a date and time
    Events, Services
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.PositiveIntegerField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=20)
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False)
    pref_email = models.BooleanField(default=False)
<<<<<<< HEAD
    call = models.BooleanField(default=False)
=======
    phone = models.BooleanField(default=False)
>>>>>>> 1746326dc8c92a96bbacac7aa8796cfb59565f18
    text = models.BooleanField(default=False)
    image2 = models.CharField(max_length=26,blank=True,default='') #url
    image3 = models.CharField(max_length=26,blank=True,default='') #url

    
class RideSharePost(ListPost):
    '''
    Class for RideShare Posts, additional attributes are trip details and 
    a bool signifying if it is a round trip or not.
    return_date_time only needed if it is a round trip
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.PositiveIntegerField()
    departure_date_time = models.DateTimeField()
    return_date_time = models.DateTimeField()
    trip = models.CharField(max_length=50)
    round_trip = models.BooleanField(default=False) 
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False)
    pref_email = models.BooleanField(default=False)
<<<<<<< HEAD
    call = models.BooleanField(default=False)
=======
    phone = models.BooleanField(default=False)
>>>>>>> 1746326dc8c92a96bbacac7aa8796cfb59565f18
    text = models.BooleanField(default=False)
    image2 = models.CharField(max_length=26,blank=True,default='') #url
    image3 = models.CharField(max_length=26,blank=True,default='') #url    
    
