from django.contrib import admin

from .models import Comments, Bids, Auction_listings, User, Watchlist

# Register your models here.
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(Auction_listings)
admin.site.register(User)
admin.site.register(Watchlist)

