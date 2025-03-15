from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bid", views.bid_view, name="bid"),
    path("categories", views.categories_view, name="categories"),
    path("category/<str:category_name>", views.category_view, name="category"),
    path("comment", views.comment_view, name="comment"),
    path("create", views.create_listing, name="create"),
    path("listing/<int:listing_id>", views.listing_view, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name="watchlist"),
]
