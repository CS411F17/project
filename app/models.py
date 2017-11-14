from django.db import models


# Create your models here.
class Restaurants(models.Model):
    r_id = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    food_type = models.CharField(max_length=50)
    image_url = models.URLField()
    yelp_url = models.URLField()
    phone = models.CharField(max_length=50)
    rating = models.FloatField()
    category_one = models.CharField(max_length=50)

    def __str__(self):
        return (self.name, self.location)


class UserRequest(models.Model):
    location = models.CharField(max_length=30)
    term = models.CharField(max_length=30)

    def __str__(self):
        return (self.location, self.term)
