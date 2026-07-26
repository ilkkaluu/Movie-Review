from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):
	title = models.CharField(max_length=200)
	year = models.PositiveSmallIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["title", "year"], name="unique_movie_title_year"),
		]
		ordering = ["title", "year"]

	def __str__(self):
		return f"{self.title} ({self.year})"


class WatchedMovie(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watched_movies")
	title = models.CharField(max_length=200)
	year = models.PositiveSmallIntegerField()
	added_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["user", "title"], name="unique_watched_movie_per_user"),
		]
		ordering = ["title", "year"]

	def __str__(self):
		return f"{self.title} ({self.year})"


class MovieReview(models.Model):
	watched_movie = models.OneToOneField(WatchedMovie, on_delete=models.CASCADE, related_name="review")
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	review_text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["watched_movie__title"]

	def __str__(self):
		return f"{self.watched_movie.title}: {self.rating}/5"
