from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("movies/", views.movie_list, name="movie-list"),
    path("movies/add-to-watched/", views.add_to_watched_movies, name="add-to-watched-movie"),
    path("movies/<int:watched_movie_id>/review/", views.leave_review, name="leave-review"),
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]