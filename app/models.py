from django.db import models


# Create your models here.
class Restaurants(models.Model):
    r_id = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    food_type = models.CharField(max_length=50, null=True)
    image_url = models.URLField(null=True)
    yelp_url = models.URLField(null=True)
    phone = models.CharField(max_length=50, null=True)
    rating = models.FloatField(null=True)
    category_one = models.CharField(max_length=50, null=True)

    def __str__(self):
        return (self.name, self.location)


class UserRequest(models.Model):
    location = models.CharField(max_length=30, null=True)
    term = models.CharField(max_length=30, null=True)

    def __str__(self):
        return (self.location, self.term)


class UserInfo(models.Model):
    name = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    hometown = models.CharField(max_length=30, null=True)
    num_friends = models.IntegerField(null=True)
    age_range = models.IntegerField(null=True)
    religion = models.CharField(max_length=20, null=True)
    education = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name
