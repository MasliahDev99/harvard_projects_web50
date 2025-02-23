from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import json

from .models import User,Post,Follow,Like


# We define a global variable for max post per page
MAX_POSTS_PER_PAGE = 10

def index(request):
    # Obtener todos los posts ordenados por fecha
    all_posts = Post.objects.all().order_by('-timestamp')

    # Configurar paginación
    paginator = Paginator(all_posts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get('page', 1)

    try:
        page_posts = paginator.page(page_number)
    except PageNotAnInteger:
        page_posts = paginator.page(1)
    except EmptyPage:
        page_posts = paginator.page(paginator.num_pages)

    # Lista de posts que el usuario ha dado like
    liked = []

    # Recorrer los posts paginados
    for post in page_posts:
        # Contar likes para todos los usuarios
        post.likes = Like.objects.filter(post=post).count()

        # Si el usuario está autenticado, verificar qué posts ha dado like
        if request.user.is_authenticated:
            if Like.objects.filter(user=request.user, post=post).exists():
                liked.append(post.id)

    context = {
        "page_posts": page_posts,
        "liked": liked,  # Solo se llenará si el usuario está autenticado
    }
    return render(request, "network/index.html", context)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

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
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")


@login_required
def post(request):  
    if request.method == "POST":
        content = request.POST.get('content')
        created_by = request.user
        if not content:
            messages.error(request, 'Post content cannot be empty.')
            return HttpResponseRedirect(reverse("network:index"))

        new_post = Post(content=content,user=created_by)
        new_post.save()

        messages.success(request, 'Post created successfully.')
        return HttpResponseRedirect(reverse("network:index"))



@login_required
def profile(request, id):
    try:
        # Get the profile user by the URL id parameter, not the logged-in user
        profile_user = User.objects.get(pk=id)
        
        # Get correct follower and following counts
        followers_count = Follow.objects.filter(following=profile_user).count()
        following_count = Follow.objects.filter(follower=profile_user).count()
        
        # Check if logged-in user is following the profile user
        is_following = Follow.objects.filter(
            follower=request.user, 
            following=profile_user
        ).exists() if request.user.is_authenticated else False

        # Get post count and posts
        post_count = Post.objects.filter(user=profile_user).count()
        posts = Post.objects.filter(user=profile_user).order_by("-timestamp")

        # Pagination
        paginator = Paginator(posts, MAX_POSTS_PER_PAGE)
        page_number = request.GET.get('page', 1)
        
        try:
            page_posts = paginator.page(page_number)
        except PageNotAnInteger:
            page_posts = paginator.page(1)
        except EmptyPage:
            page_posts = paginator.page(paginator.num_pages)

        context = {
            "profile_user": profile_user,
            "followers_count": followers_count,
            "following_count": following_count,
            "is_following": is_following,
            "post_count": post_count,
            "page_posts": page_posts,
        }
        return render(request, "network/profile.html", context)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("network:index"))




@login_required
def follow(request, user_id):
    if request.method == "POST":
        try:
            user_to_follow = User.objects.get(pk=user_id)
            if request.user != user_to_follow:
                follow_obj, created = Follow.objects.get_or_create(
                    follower=request.user,
                    following=user_to_follow
                )
                if not created:
                    follow_obj.delete()
        except User.DoesNotExist:
            pass
    return HttpResponseRedirect(reverse("network:profile", args=[user_id]))


def following(request):
    currentUser = User.objects.get(pk=request.user.id)

    followings = Follow.objects.filter(follower=currentUser)
    followingPosts = Post.objects.filter(user__in=followings.values_list('following')).order_by('-id')


    paginator = Paginator(followingPosts, MAX_POSTS_PER_PAGE)
    page_number = request.GET.get('page',1)

    try:
        page_posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_posts = paginator.get_page(1)
    except EmptyPage:
        page_posts = paginator.get_page(paginator.num_pages)


    liked = []
  

    for post in page_posts:
        if Like.objects.filter(user=request.user, post=post).exists():
            liked.append(post.id)
        
        post.likes = Like.objects.filter(post=post).count()

    context = {
        "page_posts": page_posts,
        "liked": liked,
    }
    return render(request, "network/following.html", context)




@login_required
def toggle_like(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        user = request.user
        # Buscar si ya existe un like para este usuario y post
        like = Like.objects.filter(user=user, post=post)
        if like.exists():
            like.delete()
            liked = False
        else:
            Like.objects.create(user=user, post=post)
            liked = True
        # Contar los likes usando el modelo Like, no un atributo de Post
        like_count = Like.objects.filter(post=post).count()
        return JsonResponse({"success": True, "liked": liked, "like_count": like_count}, status=200)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



        

@login_required
def edit_post(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
        if post.user != request.user:
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        data = json.loads(request.body)
        new_content = data.get('content', '').strip()
        
        if new_content:
            post.content = new_content
            post.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Content cannot be empty'}, status=400)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

    

