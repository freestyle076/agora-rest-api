from django.db import models
'''
Object-relational models for database tables. Each class represents
a MySQL schema; Django handles managing the database to mirror the classes
found below.
'''


class User(models.Model):
    '''
    User schema class model. Holds information on the user and the user's
    contact information.
    '''
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    gonzaga_email = models.EmailField(unique=True)
    pref_email = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=11,null=True,blank=True)

