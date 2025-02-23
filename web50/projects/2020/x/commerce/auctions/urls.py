from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.home, name="home"),   
    path("auctions/", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create, name="create"),
    path("watchlist/", views.wathclist_view, name="watchlist"),
    path("watchlist/add/<int:auction_id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("categories/", views.categories, name="categories"),
    path("categories/<str:category_name>/", views.category_auctions, name="category"),
    path("delete/<int:auction_id>/", views.delete_auction, name="delete_auction"),
    path("bid_history/", views.bid_history, name="bid_history"),
    path("closed_listings/", views.closed_listings, name="closed_listings"),
    path("listing/<int:auction_id>/", views.listing_detail, name="listing_detail"),
    path("listing/<int:auction_id>/bid/", views.place_bid, name="place_bid"),
    path('comments/<int:auction_id>/', views.comments, name='auction_comments'),
    path('comments/<int:auction_id>/reply/<int:comment_id>/', views.comment_reply, name='comment_reply'),
    path('comments/<int:auction_id>/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('comments/<int:auction_id>/update/<int:comment_id>/', views.update_comment, name='update_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
