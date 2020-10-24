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
    # liked posts get
    liked = Post.objects.filter(
            liked_user_count=request.user.id
        ).all().values()

    if request.user.id:
        user = User.objects.get(id=request.user.id)
        requested_list = user.requesting.all().values()
    else:
        requested_list = []

    liked_posts = []
    for i in range(len(liked)):
        liked_posts.append(liked[i]["id"])
    # Show 10 posts per page.
    paginator = Paginator(posts, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, "facebook/index.html", {'posts': posts, "users": users,'page_obj': page_obj, 'liked_posts': liked_posts, 'requested' : requested_list })

@csrf_exempt
@login_required
def following_posts(request):
    users = User.objects.all()
    # liked posts get
    liked = Post.objects.filter(
            liked_user_count=request.user.id
        ).all().values()
    liked_posts = []
    for i in range(len(liked)):
        liked_posts.append(liked[i]["id"])
    posts = []
    # Show 5 posts per page.
    paginator = Paginator(posts, 5) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, "facebook/following_posts.html", {'posts': posts, "users": users,'page_obj': page_obj, 'liked_posts': liked_posts, 'following_users' : following_users})

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            user = User.objects.get(
                id=request.user.id
            )
            user.is_online = 1
            user.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "facebook/index.html", {
                "message": "Invalid username and/or password."
            })


def logout_view(request):
    user = User.objects.get(
            id=request.user.id
            )
    user.is_online = 0
    user.save()
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        Birthdate_Day = request.POST["Day"]
        Birthdate_Month = request.POST["Month"]
        Birthdate_Year = request.POST["Year"]
        Gender = request.POST['gender']

        password = request.POST["password"]
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, password)
            user.first_name = first_name
            user.last_name = last_name
            user.Birthdate_Day = Birthdate_Day
            user.Birthdate_Month = Birthdate_Month
            user.Birthdate_Year = Birthdate_Year
            user.Gender = Gender
            user.save()
        except IntegrityError:
            print("Username already taken.")
            return render(request, "facebook/index.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))


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

def profile(request, profile_id):
    profile = User.objects.get(
            id=profile_id
            )
    friend_list = User.objects.filter(
            friends=request.user.id
        ).all().values()

    if request.user.id:
        user = User.objects.get(id=request.user.id)
        requested_list = user.requesting.all().values()
    else:
        requested_list = []
    if friend_list:
        for friend in friend_list:
            if friend["id"] == profile_id:
                friends = True
            else:
                friends = False
    else:
        friends = False

    users = User.objects.all()
    # liked posts get
    liked = Post.objects.filter(
            liked_user_count=request.user.id
        ).all().values()
    liked_posts = []
    for i in range(len(liked)):
        liked_posts.append(liked[i]["id"])
    posts = Post.objects.all().filter(
            username_id=profile_id
        ).order_by("-timestamp").all()
    # Show 5 posts per page.
    paginator = Paginator(posts, 5) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    day_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    year_list = [2019,2018,2017,2016,2015,2014,2013,2012,2011,2010,2009,2008,2007,2006,2005,2004,2003,2002,2001,2000,1999,1998,1997,1996,1995,1994,1993,1992,1991,1990,1989,1988,1987,1986,1985,1984,1983,1982,1981,1980,1979,1978,1977,1976,1975,1974,1973,1972,1971,1970,1969,1968,1967,1966,1965,1964,1963,1962,1961,1960,1959,1958,1957,1956,1955,1954,1953,1952,1951,1950,1949,1948,1947,1946,1945,1944,1943,1942,1941,1940,1939,1938,1937,1936,1935,1934,1933,1932,1931,1930,1929,1928,1927,1926,1925,1924,1923,1922,1921,1920,1919,1918,1917,1916,1915,1914,1913,1912,1911,1910,1909,1908,1907,1906,1905,1904,1903,1902,1901]

    return  render(request, "facebook/profile.html", 
    {'profile': profile,
    'posts': posts, 
    "users": users,
    'page_obj': page_obj, 
    'liked_posts': liked_posts, 
    'friends': friends, 
    'requested' : requested_list, 
    'day_list': day_list,
    'month_list': month_list,
    'year_list': year_list,
    
     })

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
        return render(request, "facebook/edit_profile.html")
    try:
        user = User.objects.get(username=request.user)
        avatar_id = request.POST["avatar"]
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email      not found."}, status=404)
    
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
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    post.body = data["body"]
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
        for like in likes:
            post.liked_user_count.remove(like)
            profile.like_count = profile.like_count - 1
        post.delete()
        profile.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "ID's not matching"}, status=400)

@csrf_exempt
@login_required
def send_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        requested_user = User.objects.get(id=data["profile_id"])
        print(requested_user)
        requested_user.requesting.add(request.user.id)
        requested_user.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)


@csrf_exempt
@login_required
def unsend_request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        requested_user = User.objects.get(id=data["profile_id"])
        requested_user.requesting.remove(request.user.id)
        requested_user.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)

@csrf_exempt
@login_required
def delete_friend(request):
    if request.method == "POST":
        data = json.loads(request.body)  
        requested_user = User.objects.get(id=data["profile_id"])
        requested_user_2 = User.objects.get(id=request.user.id)
        requested_user.friends.remove(request.user.id)
        requested_user_2.friends.remove(data["profile_id"])
        requested_user.save()
        requested_user_2.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)

@csrf_exempt
@login_required
def accept(request):
    if request.method == "POST":
        data = json.loads(request.body)
        requested_user = User.objects.get(id=request.user.id)
        requested_user_2 = User.objects.get(id=data["profile_id"])
        requested_user.requesting.remove(data["profile_id"])
        requested_user.friends.add(data["profile_id"])
        requested_user_2.friends.add(request.user.id)
        requested_user.save()
        requested_user_2.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)

@csrf_exempt
@login_required
def deny(request):
    if request.method == "POST":
        data = json.loads(request.body)
        requested_user = User.objects.get(id=request.user.id)
        requested_user.requesting.remove(data["profile_id"])
        requested_user.save()
        return HttpResponse(status=204)
    else:
        return HttpResponse(status=404)
