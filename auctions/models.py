from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    categories = [
        ("ELC","Electronics"),
        ("FUR","Furniture"),
        ("BOK","Books"),
        ("CLO","Clothing"),
        ("OTH","Other"),
    ]

    itemName = models.CharField(max_length=100)
    min = models.FloatField(default=0)
    description = models.CharField(max_length=200, default="")
    category = models.CharField(max_length=3,choices=categories, null=True, blank=True)
    image = models.ImageField(upload_to="listing_images",null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    comments = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name="comments",null=True, blank=True)
    

    def __str__(self):
        return self.itemName
    

class Bid(models.Model):    
    listing = models.OneToOneField('Listing', on_delete=models.SET_NULL, null = True, blank=True,related_name="bid")
    highestBidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="bids_placed")
    highestBidAmount = models.FloatField(default=0.0)
    totalBids = models.PositiveIntegerField(default=0)  

    def place_bid(self, amount, user):
        if amount <= self.listing.min:
            raise ValueError("Bid must be higher than minimum price.")
        if amount <= self.highestBidAmount:
            raise ValueError("Bid must be higher than current highest bid.")
        
        self.highestBidAmount = amount
        self.highestBidder = user
        self.totalBids += 1
        self.save()

    def __str__(self):
        return f"{self.listing}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="comments")
    comment = models.CharField(max_length=400, default="")

    def __str__(self):
        return f"{self.user}"

