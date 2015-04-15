from django.db import models
import datetime

def default_refresh_date():
    return datetime.date.today() + datetime.timedelta(days=-1)

class ListPost(models.Model):
    '''
    Class for storing data on our post and displaying in List Format
    '''
    display_value = models.CharField(max_length=150)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=30)
    post_date_time = models.DateTimeField() #creation/refresh date_time
    report_count = models.PositiveSmallIntegerField(default=0) 
    deleted = models.BooleanField(default=False) #hides from display on UI
    last_refresh_date = models.DateField(default=default_refresh_date)
    image1 = models.CharField(max_length=50,blank=True,default='') #url
    
    class Meta:
        abstract = True

class ItemPost(ListPost):
    '''
    Items works for our item categories
    Electronics, furniture, appliances/kitchen, and recreation
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False) #contact option
    pref_email = models.BooleanField(default=False) #contact option
    call = models.BooleanField(default=False) #contact option
    text = models.BooleanField(default=False) #contact option
    image2 = models.CharField(max_length=50,blank=True,default='') #url
    image3 = models.CharField(max_length=50,blank=True,default='') #url
    
class BookPost(ListPost):
    '''
    Class for Books, additional Attribute is ISBN
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    isbn = models.CharField(max_length=13)
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False) #contact option
    pref_email = models.BooleanField(default=False) #contact option
    call = models.BooleanField(default=False) #contact option
    text = models.BooleanField(default=False) #contact option
    image2 = models.CharField(max_length=50,blank=True,default='') #url
    image3 = models.CharField(max_length=50,blank=True,default='') #url

    
class DateLocationPost(ListPost):
    '''
    Class for categories that require a date and time
    Events, Services
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    date_time = models.DateTimeField(null=True)
    location = models.CharField(max_length=70)
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False) #contact option
    pref_email = models.BooleanField(default=False) #contact option
    call = models.BooleanField(default=False) #contact option
    text = models.BooleanField(default=False) #contact option
    image2 = models.CharField(max_length=50,blank=True,default='') #url
    image3 = models.CharField(max_length=50,blank=True,default='') #url

    
class RideSharePost(ListPost):
    '''
    Class for RideShare Posts, additional attributes are trip details and 
    a bool signifying if it is a round trip or not.
    return_date_time only needed if it is a round trip
    '''
    description = models.CharField(max_length=1000,blank=True,default='')
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    departure_date_time = models.DateTimeField(null=True)
    return_date_time = models.DateTimeField(null=True)
    trip = models.CharField(max_length=150)
    round_trip = models.BooleanField(default=False) 
    username = models.ForeignKey('user_service.User')
    gonzaga_email = models.BooleanField(default=False) #contact option
    pref_email = models.BooleanField(default=False) #contact option
    call = models.BooleanField(default=False) #contact option
    text = models.BooleanField(default=False) #contact option
    image2 = models.CharField(max_length=50,blank=True,default='') #url
    image3 = models.CharField(max_length=50,blank=True,default='') #url    
    
class PostReport(models.Model):
    post_id = models.IntegerField()
    category = models.CharField(max_length=50)
    username = models.ForeignKey('user_service.User')
