from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Importing our models
from .models import Bid, Comment, Listing, User

# Declaration of the categories Global variable
categories = set()


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

# This view handles creating a new Listing and rendering the Create Listing page
@login_required
def create_listing(request):
    if request.POST:
        # Handles the form (with POST method) from the create new listing page
        title = request.POST.get("title")
        description = request.POST.get("description")
        # The price could be type casted to integer
        price =  float(request.POST.get("price"))
        image = request.POST.get("image")
        category = request.POST.get("category")
        new_listing = Listing(name=title, description=description, price=price, image=image, category=category)
        new_listing.save()
        categories.add(category)
        return HttpResponseRedirect(reverse("index"))
    # Renders the create listing page when there is a GET method
    return render(request, "auctions/create_listing.html")


# Function defined to handle the watchlist page
watchlist_items = []
@login_required
def watchlist(request):
    if request.POST:
        item_id = request.POST["item"]
        item = Listing.objects.get(id=item_id)
        if item in watchlist_items:
            # Remove listing from watchlist
            watchlist_items.remove(item)
        else:
            # Add listing to watchlist
            watchlist_items.append(item)
    return render(request, "auctions/watchlist.html", {
         "items" : watchlist_items,
     })

# Function defined to handle the listing page
def listing_view(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    bids = listing.bid_item.all()
    comments = listing.comment_item.all()
    return render(request, "auctions/listing.html", {
        "listing" : listing,
        "bids" : bids,
        "comments" : comments,
    }) 

# Function that handles bids
@login_required
def bid_view(request):

    # Handles the Bid form
    if request.POST:
        amount = request.POST.get("bid")
        listing_id = request.POST.get("listing")
        listing = Listing.objects.get(id=listing_id)
        bid = Bid(listing=listing, amount=amount)
        bid.save()
        return HttpResponseRedirect(reverse('listing', args=listing_id,))
    return HttpResponseRedirect(reverse('index'))

# The Comment view for handling comments on listing
def comment_view(request):
    if request.POST:
        comment = request.POST.get("comment")
        listing_id = request.POST.get("listing")
        listing = Listing.objects.get(id=listing_id)
        comment = Comment(listing=listing, comment=comment)
        comment.save()
        return HttpResponseRedirect(reverse('listing', args=listing_id))
    return HttpResponseRedirect(reverse('index'))

# The categories view for rendering the categories page
def categories_view(request):
    return render(request, "auctions/categories.html", {
        "categories" : categories,
    })

def category_view(request, category_name):
    return