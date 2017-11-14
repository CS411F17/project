from django.db import models


# Create your models here.
class Restaurants(models.Model):
    restaurantName = models.CharField(max_length=50)
    restaurantLocation = models.CharField(max_length=50)
    foodType = models.CharField(max_length=50)

    def __str__(self):
        return self.restaurantName


class UserRequest(models.Model):
    location = models.CharField(max_length=15)
    term = models.CharField(max_length=15)

    def __str__(self):
        return (self.location, self.term)
