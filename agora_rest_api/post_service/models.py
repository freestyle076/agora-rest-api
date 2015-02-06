from django.db import models
import datetime
class ListPost(models.Model):
    '''
    Class for storing data on our post and displaying in List Format
    '''
    display_value = models.CharField(max_length=40)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    post_date_time = models.DateTimeField()
    report_count = models.PositiveSmallIntegerField(default=0)
    last_refresh_date = models.DateField(default=datetime.date.today)
    image1 = models.CharField(max_length=50,blank=True,default='') #url
    
    class Meta:
        abstract = True

class ItemPost(ListPost):
    '''
    Items works for our item categories
    Electronics, furniture, appliances/kitchen, and recreation
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.DecimalField(max_digits=6,decimal_places=2)
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False)
    pref_email = models.BooleanField(default=False)
    call = models.BooleanField(default=False)
    text = models.BooleanField(default=False)
    image2 = models.CharField(max_length=50,blank=True,default='') #url
    image3 = models.CharField(max_length=50,blank=True,default='') #url
    
class BookPost(ListPost):
    '''
    Class for Books, additional Attribute is ISBN
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.DecimalField(max_digits=6,decimal_places=2)
    isbn = models.CharField(max_length=12)
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False)
    pref_email = models.BooleanField(default=False)
    call = models.BooleanField(default=False)
    text = models.BooleanField(default=False)
    image2 = models.CharField(max_length=50,blank=True,default='') #url
    image3 = models.CharField(max_length=50,blank=True,default='') #url

    
class DateLocationPost(ListPost):
    '''
    Class for categories that require a date and time
    Events, Services
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.DecimalField(max_digits=6,decimal_places=2)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=70)
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False)
    pref_email = models.BooleanField(default=False)
    call = models.BooleanField(default=False)
    text = models.BooleanField(default=False)
    image2 = models.CharField(max_length=50,blank=True,default='') #url
    image3 = models.CharField(max_length=50,blank=True,default='') #url

    
class RideSharePost(ListPost):
    '''
    Class for RideShare Posts, additional attributes are trip details and 
    a bool signifying if it is a round trip or not.
    return_date_time only needed if it is a round trip
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.DecimalField(max_digits=6,decimal_places=2)
    departure_date_time = models.DateTimeField()
    return_date_time = models.DateTimeField(null=True)
    trip = models.CharField(max_length=50)
    round_trip = models.BooleanField(default=False) 
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False)
    pref_email = models.BooleanField(default=False)
    call = models.BooleanField(default=False)
    text = models.BooleanField(default=False)
    image2 = models.CharField(max_length=50,blank=True,default='') #url
    image3 = models.CharField(max_length=50,blank=True,default='') #url    
    
class PostReport(models.Model):
    post_id = models.IntegerField()
    category = models.CharField(max_length=50)
    username = models.ForeignKey('user_service.User')
