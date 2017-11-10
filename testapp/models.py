from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
import hashlib
# Create your models here.
class Restaurants(models.Model):
	restaurantName = models.CharField(max_length = 50)
	restaurantLocation = models.CharField(max_length = 50)
	foodType = models.CharField(max_length = 50)

	def __str__(self):
		return self.restaurantName

class UserInfo(models.Model):
	name = models.CharField(max_length = 50)
	location = models.CharField(max_length = 30)
	hometown = models.CharField(max_length = 30)
	num_friends = models.IntegerField()
	age_range = models.IntegerField()
	religion = models.CharField(max_length = 20)
	education = models.CharField(max_length = 30)

	def __str__(self):
		return self.name

class UserRequest(models.Model):
  	location = models.CharField(max_length=15)
  	term = models.CharField(max_length=15)

  	def __str__(self):
    	return (self.location, self.term)