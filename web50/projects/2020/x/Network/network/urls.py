
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/", views.post, name="post"),
    path("profile/<int:id>", views.profile, name="profile"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("following/", views.following, name="following"),
    path("like/<int:post_id>/", views.toggle_like, name="like"),
    path("edit/<int:post_id>/", views.edit_post, name="edit_post"),
]
