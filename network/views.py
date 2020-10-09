import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    posts = Post.objects.all().order_by("-timestamp").all()
    users = User.objects.all()
    topuser = User.objects.all().order_by("-like_count").first()
    # liked posts get
    liked = Post.objects.filter(
            liked_user_count=request.user.id
        ).all().values()
    liked_posts = []
    for i in range(len(liked)):
        liked_posts.append(liked[i]["id"])
    # Following users get
    following = User.objects.filter(
            followers=request.user.id
        ).all().values()
    following_users = []
    for i in range(len(following)):
        following_users.append(following[i]["id"])
    # Show 10 posts per page.
    paginator = Paginator(posts, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, "network/index.html", {'posts': posts, "users": users,'page_obj': page_obj, 'liked_posts': liked_posts, 'following_users' : following_users, "topuser": topuser})

@csrf_exempt
@login_required
def following_posts(request):
    users = User.objects.all()
    topuser = User.objects.all().order_by("-like_count").first()
    # liked posts get
    liked = Post.objects.filter(
            liked_user_count=request.user.id
        ).all().values()
    liked_posts = []
    for i in range(len(liked)):
        liked_posts.append(liked[i]["id"])
    # Following users get
    following = User.objects.filter(
            followers=request.user.id
        ).all().values()
    following_users = []
    for i in range(len(following)):
        following_users.append(following[i]["id"])

    if following_users:

        posts = Post.objects.all().filter(
                username_id__in=following_users
            ).order_by("-timestamp").all()
    else:
        posts = []
    # Show 5 posts per page.
    paginator = Paginator(posts, 5) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, "network/following_posts.html", {'posts': posts, "users": users,'page_obj': page_obj, 'liked_posts': liked_posts, 'following_users' : following_users, 'topuser': topuser})

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        avatar_id = request.POST["avatar"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.avatar = avatar_id
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def new_post(request):
        # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)  
    post = Post(
            username=request.user,
            body=data.get("body", ""),
        )
    post.save()  
    return JsonResponse({"message": "Post was saved successfully."}, status=201)    

def profile(request,profile_id):
    profile = User.objects.get(
            id=profile_id
            )
    users = User.objects.all()
    topuser = User.objects.all().order_by("-like_count").first()
    # liked posts get
    liked = Post.objects.filter(
            liked_user_count=request.user.id
        ).all().values()
    liked_posts = []
    for i in range(len(liked)):
        liked_posts.append(liked[i]["id"])
    # Following users get
    following = User.objects.filter(
            followers=request.user.id
        ).all().values()
    following_users = []
    for i in range(len(following)):
        following_users.append(following[i]["id"])

    posts = Post.objects.all().filter(
            username_id=profile_id
        ).order_by("-timestamp").all()
    # Show 5 posts per page.
    paginator = Paginator(posts, 5) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return  render(request, "network/profile.html", {'profile': profile,'posts': posts, "users": users,'page_obj': page_obj, 'liked_posts': liked_posts, 'following_users' : following_users, 'topuser': topuser})

@csrf_exempt
@login_required
def like_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    # Query for requested email
    try:
        post = Post.objects.get(id=data["post_id"])
        profile = User.objects.get(id=post.username_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    user = User.objects.get(username=request.user)
    post.like_count = post.like_count + 1
    post.liked_user_count.add(user.id)
    profile.like_count = profile.like_count + 1
    profile.save()
    post.save()
    return HttpResponse(status=204)

@csrf_exempt
@login_required
def unlike_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    # Query for requested email
    try:
        post = Post.objects.get(id=data["post_id"])
        profile = User.objects.get(id=post.username_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    user = User.objects.get(username=request.user)
    post.like_count = post.like_count - 1
    post.liked_user_count.remove(user.id)
    profile.like_count = profile.like_count - 1
    profile.save()
    post.save()
    return HttpResponse(status=204)

@csrf_exempt
@login_required
def follow_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    # Query for requested email
    try:
        post_user = User.objects.get(id=data["user_id"])
        user = User.objects.get(username=request.user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    post_user.followers.add(user.id)
    user.following.add(post_user.id)
    post_user.save()
    user.save()
    return HttpResponse(status=204)

@csrf_exempt
@login_required
def unfollow_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    # Query for requested email
    try:
        post_user = User.objects.get(id=data["user_id"])
        user = User.objects.get(username=request.user)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    post_user.followers.remove(user.id)
    user.following.remove(post_user.id)
    post_user.save()
    user.save()
    return HttpResponse(status=204)

@csrf_exempt
@login_required
def edit_profile(request):

    if request.method != "POST":
        return render(request, "network/edit_profile.html")
    try:
        user = User.objects.get(username=request.user)
        avatar_id = request.POST["avatar"]
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)
    
    user.avatar = avatar_id
    user.save()
    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def edit_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    # Query for requested email
    try:
        post = Post.objects.get(id=data["post_id"])
        print(data["post_id"])
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    print(post.body)
    post.body = data["body"]
    print(post.body)
    post.save()
    return HttpResponse(status=204)

@csrf_exempt
@login_required
def delete_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    # Query for requested email
    try:
        post = Post.objects.get(id=data["post_id"])
        profile = User.objects.get(id=post.username_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if post.username_id == request.user.id:
        likes = post.liked_user_count.filter(
            liked_id=data["post_id"]
        ).all()
        print()
        for like in likes:
            post.liked_user_count.remove(like)
            profile.like_count = profile.like_count - 1
        post.delete()
        profile.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "ID's not matching"}, status=400)
