from django.urls import path

from . import views

app_name = 'auctions'

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/",views.create,name="create"),
    path("watchlist/",views.wathclist_view,name="watchlist"),
    path("watchlist/add/<int:auction_id>",views.add_to_watchlist,name="add_to_watchlist"),
    path("categories/",views.categories,name="categories"),
    path("categories/<str:category_name>/",views.category_auctions,name="category"),
]
