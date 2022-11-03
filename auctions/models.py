from django.db import models
from django.db.models.fields import IntegerField
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from commerce import settings

# Create your models here.

CATEGORIES = (
    ('gr', 'groceries'),
   ('cl', 'clothing'),
   ('bk', 'books'),
   ('fn', 'furniture'),
   ('ft', 'fitness'),
   ('gm', 'games'),
   ('gd', 'gadjets'),
   ('no', 'None'),
)
#create model for Auction listings
class Auction_listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length = 500)
    price = models.IntegerField(default=0)
    image = models.URLField(max_length=200)
    date_created = models.DateField(auto_now=True, auto_now_add=False)
    created_by = models.CharField(max_length=20)
    closed = models.BooleanField(default=False)
    category = models.CharField(max_length=50, choices=CATEGORIES, default=CATEGORIES[7][1])
    def __str__(self):
        return f"{self.title}"

#create model for Bids
class Bids(models.Model):
    user = models.CharField(default="", max_length=40)
    item_id = models.IntegerField(default=0)
    bid = models.IntegerField(default=0)

#create model for comments
class Comments(models.Model):
    listing = models.IntegerField(default=0)
    name = models.CharField(max_length=64)
    email = models.EmailField(default="")
    content = models.TextField(default="")
    time_created= models.DateTimeField(auto_now_add=True)

# create model for watchlist
class Watchlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ManyToManyField(Auction_listings, related_name="items")


def __str__(self):
    return f"{self.user.username}: {self.item.Auction_listings.title}"
        


class User(AbstractUser):
    pass