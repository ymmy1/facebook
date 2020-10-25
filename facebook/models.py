from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    Birthdate_Day = models.PositiveSmallIntegerField(default=1,blank=False, null=False)
    Birthdate_Month = models.PositiveSmallIntegerField(default=1,blank=False, null=False)
    Birthdate_Year = models.PositiveSmallIntegerField(default=1,blank=False, null=False)
    Gender = models.TextField(blank=False)

    is_online = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    
    avatar = models.TextField(default="../../static/facebook/img/avatars/default.jpg")
    cover = models.TextField(default="../../static/facebook/img/avatars/green-facebook-cover-9.jpg")
    
    work = models.TextField(blank=True)
    school = models.TextField(blank=True)
    from_location = models.TextField(blank=True)
    
    requesting = models.ManyToManyField("User", related_name="requesting_id")
    friends = models.ManyToManyField("User", related_name="friends_id")


    pass


class Post(models.Model):
    username = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")
    like_count = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    liked_user_count = models.ManyToManyField("Post", related_name="liked_id")
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    img = models.TextField(blank=True, null=True)
    comments = models.ManyToManyField("Comment", related_name="post_id")
    

class Comment(models.Model):
    username = models.ForeignKey("User", on_delete=models.CASCADE, related_name="comment_user")
    body = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)

