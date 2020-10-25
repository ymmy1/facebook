
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<int:profile_id>", views.profile, name="profile"),
    path("edit", views.edit, name="edit"),
    path("unlike_post", views.unlike_post, name="unlike_post"),
    path("like_post", views.like_post, name="like_post"),
    path("new_post", views.new_post, name="new_post"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("delete_post", views.delete_post, name="delete_post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("send_request", views.send_request, name="send_request"),
    path("delete_friend", views.delete_friend, name="delete_friend"),
    path("unsend_request", views.unsend_request, name="unsend_request"),
    path("accept", views.accept, name="accept"),
    path("deny", views.deny, name="deny"),
    path("comment", views.comment, name="comment")
]
