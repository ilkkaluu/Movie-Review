from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("users/", views.search_users, name="search-users"),
    path("reviews/public/", views.public_reviews, name="public-reviews"),
    path("profile/watched-movies/", views.watched_movies_page, name="watched-movies-page"),
    path("profile/watched-movies/<int:user_id>/", views.watched_movies_user_page, name="watched-movies-user-page"),
    path("profile/reviews/", views.user_reviews_page, name="user-reviews-page"),
    path("movies/", views.movie_list, name="movie-list"),
    path("movies/add-to-watched/", views.add_to_watched_movies, name="add-to-watched-movie"),
    path("movies/<int:watched_movie_id>/review/", views.leave_review, name="leave-review"),
    path("reviews/<int:review_id>/edit/", views.edit_review, name="edit-review"),
    path("profile/", views.profile, name="profile"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]