from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("discover/", views.discover, name="discover"),
    path("communities/", views.communities, name="communities"),
    path("messages/", views.messages_page, name="messages"),
    path("profile/", views.profile, name="profile"),

    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("saved-posts/", views.saved_posts, name="saved_posts"),
    path("save-post/<int:post_id>/", views.save_post, name="save_post"),
]