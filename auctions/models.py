from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Create the Listing model that has name, description, price and image fields.
class Listing(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id} ${self.name}"

# The Bid model that has the bidding amount field
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid_item")
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True)

# The Comment model that has the comment field
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_item")
    comment = models.CharField(max_length=200, null=True)
