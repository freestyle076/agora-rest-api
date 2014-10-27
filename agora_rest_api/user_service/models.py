from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50,min_length=2)
    email = models.CharField(max_length=60,min_length=2)
    first_name = models.CharField(max_length=30,min_length=2)
    last_name = models.CharField(max_length=40,min_length=2)
    phone = models.CharField(max_length=11,min_length=10,min_length=2)