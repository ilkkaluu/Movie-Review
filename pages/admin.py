from django.contrib import admin
from .models import Movie, MovieReview, WatchedMovie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
	list_display = ("title", "year")
	search_fields = ("title",)
	ordering = ("title", "year")


@admin.register(WatchedMovie)
class WatchedMovieAdmin(admin.ModelAdmin):
	list_display = ("title", "year", "user", "added_at")
	search_fields = ("title", "user__username")
	list_filter = ("year",)
	ordering = ("title", "year")


@admin.register(MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
	list_display = ("watched_movie", "rating", "created_at", "updated_at")
	search_fields = ("watched_movie__title", "watched_movie__user__username")
	list_filter = ("rating",)
