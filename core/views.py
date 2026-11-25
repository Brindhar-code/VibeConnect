from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Post, Like, SavedPost


# -------------------------
# HOME FEED
# -------------------------

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")

        # Create a new post
        content = request.POST.get("content", "").strip()

        if content:
            Post.objects.create(
                author_name=request.user.username,
                content=content
            )

            return redirect("home")

        # Like or unlike a post
        post_id = request.POST.get("post_id")

        if post_id:
            post = get_object_or_404(Post, id=post_id)

            existing_like = Like.objects.filter(
                post=post,
                user_name=request.user.username
            )

            if existing_like.exists():
                existing_like.delete()
            else:
                Like.objects.create(
                    post=post,
                    user_name=request.user.username
                )

            return redirect("home")

    posts = Post.objects.all().order_by("-created_at")

    for post in posts:
        post.likes_count = post.likes.count()

        post.liked_by_user = (
            request.user.is_authenticated
            and Like.objects.filter(
                post=post,
                user_name=request.user.username
            ).exists()
        )

        post.is_saved = (
            request.user.is_authenticated
            and SavedPost.objects.filter(
                post=post,
                user=request.user
            ).exists()
        )

    total_posts = 0

    if request.user.is_authenticated:
        total_posts = Post.objects.filter(
            author_name=request.user.username
        ).count()

    return render(
        request,
        "core/home.html",
        {
            "posts": posts,
            "total_posts": total_posts,
        }
    )


# -------------------------
# DISCOVER
# -------------------------

def discover(request):
    posts = Post.objects.all().order_by("-created_at")

    return render(
        request,
        "core/section.html",
        {
            "section": "discover",
            "posts": posts,
        }
    )


# -------------------------
# COMMUNITIES
# -------------------------

def communities(request):
    return render(
        request,
        "core/section.html",
        {
            "section": "communities",
        }
    )


# -------------------------
# MESSAGES
# -------------------------

@login_required
def messages_page(request):
    return render(
        request,
        "core/section.html",
        {
            "section": "messages",
        }
    )


# -------------------------
# PROFILE
# -------------------------

@login_required
def profile(request):
    user_posts = Post.objects.filter(
        author_name=request.user.username
    ).order_by("-created_at")

    return render(
        request,
        "core/section.html",
        {
            "section": "profile",
            "user_posts": user_posts,
            "total_posts": user_posts.count(),
        }
    )


# -------------------------
# REGISTER
# -------------------------

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not email or not password:
            messages.error(request, "Please fill in all fields.")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("home")

    return render(request, "core/register.html")


# -------------------------
# LOGIN WITH EMAIL
# -------------------------

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user_record = User.objects.filter(
            email__iexact=email
        ).first()

        if user_record:
            user = authenticate(
                request,
                username=user_record.username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("home")

        messages.error(request, "Invalid email or password.")

    return render(request, "core/login.html")


# -------------------------
# LOGOUT
# -------------------------

def logout_view(request):
    logout(request)
    return redirect("home")


# -------------------------
# SAVED POSTS PAGE
# -------------------------

@login_required
def saved_posts(request):
    saved_items = SavedPost.objects.filter(
        user=request.user
    ).select_related("post").order_by("-saved_at")

    return render(
        request,
        "core/saved_posts.html",
        {
            "saved_items": saved_items,
        }
    )


# -------------------------
# SAVE / UNSAVE POST
# -------------------------

@login_required
@require_POST
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    saved_item = SavedPost.objects.filter(
        user=request.user,
        post=post
    )

    if saved_item.exists():
        saved_item.delete()
    else:
        SavedPost.objects.create(
            user=request.user,
            post=post
        )

    return redirect(request.META.get("HTTP_REFERER", "home"))