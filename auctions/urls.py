from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("categories", views.categories, name="categories"),
    path("groceries", views.groceries, name="groceries"),
    path("furniture", views.furniture, name="furniture"),
    path("games", views.games, name="games"),
    path("books", views.books, name="books"),
    path("fitness", views.fitness, name="fitness"),
    path("gadjets", views.gadjets, name="gadjets"),
    path("clothing", views.clothing, name="clothing"),
    path("error", views.error, name="error"),
    path("success", views.success, name="success"),
    path("comments/<int:auction_id>/", views.comment, name="comments"),
    path("active_listings", views.listings, name="active_listings"),
   path("watchlist_add/<int:auction_id>/", views.watchlist_add, name="watchlist_add"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close_auction/<int:auction_id>/", views.close, name="close"),
    path("active_listings/<int:auction_id>/", views.list_item, name="details"),
]   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)