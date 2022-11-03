from sqlite3 import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from flask_login import login_required
from django.contrib.auth.decorators import login_required

from .forms import Create_form, Comment_form, Bid_form
from .models import Auction_listings, Bids, Comments, Watchlist, User

from django.contrib import messages

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    return HttpResponseRedirect(reverse("active_listings"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            }) 
    
    else:
        return render(request, "auctions/login.html")

#log user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "passwords must match"
            })

         # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "credentials already exist"
            })
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    # on submission of the form check if the form is valid and assign the input values to variables
    if request.method == "POST":
        form = Create_form(request.POST or None)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            date = form.cleaned_data["date_created"]
            category = form.cleaned_data["categories"]
            user = request.user

            auction = Auction_listings(title=title,
                        description=description,
                        price=price,
                        image=image,
                        date_created=date,
                        category=category,
                        created_by=user
            )
            #if length of image is less than or equal to 200, save image, else return error message and render create listing page with the form
            if len(image) <=200:
                auction.save()
                return HttpResponseRedirect(reverse('success'))
            else:
                message="Image exceeds recommended limit of 200"
                return render(request, "auctions/create_listing.html", {
                    "form":Create_form,
                    "message":message
                })
    # if the page is being requested for, display the create listings page containing the form
    else:
        form = Create_form()
    return render(request, "auctions/create_listing.html", {
        "form":Create_form
    })

@login_required
def categories(request):
    return render(request, "auctions/categories.html")

@login_required
def list_item(request, auction_id):
    if request.method == "POST":
        #check if a form was submitted and exists
        form = Bid_form(request.POST or None)

        #if valid form exists assign input values to variables
        if form.is_valid():
            bid=form.cleaned_data["bid"]
            object=get_object_or_404(Auction_listings, pk=auction_id)
            item_id = object.id
            price=object.price
            username=request.user

            # if the input for bid is less than the stated price for the item, display error message
            if bid < price:
                message = "Bid must exceed initial price"
                title = get_object_or_404(Auction_listings, pk=auction_id)
                context = {
                    "message":message,
                    "title":title,
                    "comment_form":Comment_form,
                    "bid_form":Bid_form
                }
                return render(request, "auctions/list_items.html", context)
           
            #check through the Bids table for bids     
            total_bids = Bids.objects.filter(item_id=item_id).values()

            # if the length of all bids is zero, save bid
            if len(total_bids) == 0:
                bids=Bids(
                    user=username,
                    item_id=item_id,
                    bid=bid
                    )
                
                bids.save()
                
                bid_message = "Congratulations, Bid won!"
                title = get_object_or_404(Auction_listings, pk=auction_id)
                context = {
                    "bid_message": bid_message,
                    "title":title,
                    "comment_form":Comment_form,
                    "bid_form":Bid_form
                }
                return render(request, "auctions/list_items.html", context)    

            #loop through bids, if current bid exceeds old bid return a success message, else return a failure message
            for each_bid in total_bids:
                old_bid = each_bid["bid"]
                if bid > old_bid:
                    cmessage="Bid won!"
                else:
                    cmessage="Bid does not exceed existing bid"

            bids=Bids(
                user=username,
                item_id=item_id,
                bid=bid
            )

            #save bid display list items template with the item, title, comment form and bid form
            bids.save()
            title=get_object_or_404(Auction_listings, pk=auction_id)
            context= {
                "bid_message":cmessage,
                "title":title,
                "comment_form":Comment_form,
                "bid_form":Bid_form
            }
            return render(request, "auctions/list_items.html", context)

    #if request method is GET
    title = get_object_or_404(Auction_listings, pk=auction_id)
    comments = Comments.objects.filter(listing=auction_id)    
    context = {
        "title":title,
        "comments":comments,
        "comment_form":Comment_form,
        "bid_form":Bid_form
    }
    return render(request, "auctions/list_items.html", context)



def comment(request, auction_id):
    if request.method == "POST":
        #check if there is a submitted form
        form = Comment_form(request.POST or None)
        #if the submitted form is valid assign the form fields data to variables
        if form.is_valid():
            listing_id = auction_id
            name=form.cleaned_data["name"]
            email=form.cleaned_data["email"]
            content=form.cleaned_data["content"]

            comments=Comments(
                listing=listing_id,
                name=name,
                email=email,
                content=content
            )
            #save comment and redirect
            comments.save()
            return redirect ("details", auction_id)


@login_required
def listings(request):
    listings=Auction_listings.objects.all()
    return render(request, "auctions/active_listings.html", {"listings":listings})



@login_required
def watchlist(request):
    #assign object values from Watchlist model which is a foreign key to a variable
    watchlist = Watchlist.item.through.objects.all().values()
    
    #assign dictionary of all items to list of id
    list_of_id = []

    #loop through 'watchlist', assign particular auction listing id to a variable and append list of id variable to Auction listings
    for x in watchlist:
        auction_id = x['auction_listings_id']
        list_of_id.append(Auction_listings.objects.get(pk=auction_id))
    
    #print list of id 
    print(list_of_id)
    return render(request, "auctions/watchlist.html",{"watchlist": list_of_id})



@login_required
def watchlist_add(request, auction_id):
    item = get_object_or_404(Auction_listings, pk=auction_id)
    # Check if the item already exists in that user watchlist
    if Watchlist.objects.filter(user=request.user, item=item.id).exists():
        messages.add_message(request, messages.ERROR, "You already have it in your watchlist.")
        return HttpResponseRedirect(reverse("index"))
        # Get the user watchlist or create it if it doesn't exists
    user_list, created = Watchlist.objects.get_or_create(user=request.user)
    # Add the item through the ManyToManyField (Watchlist => item)
    user_list.item.add(item)
    messages.add_message(request, messages.SUCCESS, "Successfully added to your watchlist")
    return redirect("watchlist")


@login_required
def close(request, auction_id):
    if request.method == "POST":
        #Assign the auction to a variable and set that variables boolean value of closed to 'true'
        object = Auction_listings(pk=auction_id)
        object.closed=True
        #update the auction to reflect being closed
        object.save(update_fields=['closed'])
        return redirect("details", auction_id)


def groceries(request):
    groceries=Auction_listings.objects.filter(category="gr")
    return render(request, "auctions/groceries.html", {"groceries": groceries})

def clothing(request):
    clothing=Auction_listings.objects.filter(category="cl")
    return render(request, "auctions/clothing.html", {"clothing": clothing})

def books(request):
    books=Auction_listings.objects.filter(category="bk")
    return render(request, "auctions/books.html", {"books": books})

def furniture(request):
    furniture=Auction_listings.objects.filter(category="fn")
    return render(request, "auctions/furniture.html", {"furniture": furniture})

def fitness(request):
    fitness=Auction_listings.objects.filter(category="ft")
    return render(request, "auctions/fitness.html", {"fitness": fitness})

def games(request):
    furniture=Auction_listings.objects.filter(category="gm")
    return render(request, "auctions/games.html", {"games": games})

def gadjets(request):
    gadjets=Auction_listings.objects.filter(category="gd")
    return render(request, "auctions/gadjets.html", {"gadjets": gadjets})

def success(request):
    return render(request, "auctions/success.html")

def error(request):
    return render(request, "auctions/error.html")










