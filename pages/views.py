from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.db import connection
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .forms import MovieReviewForm
from .models import Movie, MovieReview, WatchedMovie


class ShortAuthenticationForm(AuthenticationForm):
	error_messages = {
		**AuthenticationForm.error_messages,
		"invalid_login": "Invalid username or password.",
	}


def home(request):
	return render(request, "home.html")


def public_reviews(request):
	reviews = (
		MovieReview.objects.filter(is_private=False)
		.select_related("watched_movie", "watched_movie__user")
		.order_by("-created_at")
	)
	return render(request, "reviews/public_reviews.html", {"reviews": reviews})


@login_required
def search_users(request):
	search_query = request.GET.get("q", "").strip()
	if len(search_query) >= 2:
		# A03 Injection demo:
		# To make the fix active, comment out below and uncomment the fix.
		with connection.cursor() as cursor:
			cursor.execute(
				f"SELECT id, username FROM auth_user WHERE username LIKE '%{search_query}%' ORDER BY username"
			)
			rows = cursor.fetchall()
		users = [{"id": row[0], "username": row[1]} for row in rows]

		# Fix for A03 Injection:
		# with connection.cursor() as cursor:
		# 	cursor.execute(
		# 		"SELECT id, username FROM auth_user WHERE username LIKE %s ORDER BY username",
		# 		[f"%{search_query}%"],
		# 	)
		# 	rows = cursor.fetchall()
		# users = [{"id": row[0], "username": row[1]} for row in rows]

		result_message = f'Search results for "{search_query}".'
		if not users:
			result_message = f'No users found with "{search_query}".'
	elif search_query:
		users = []
		result_message = "Enter at least 2 characters to search for a username."
	else:
		users = []
		result_message = "Search for a username to see matching users."

	return render(
		request,
		"users/search_users.html",
		{
			"users": users,
			"search_query": search_query,
			"result_message": result_message,
		},
	)


def movie_list(request):
	search_query = request.GET.get("q", "").strip()
	show_all = request.GET.get("all") == "1"
	movie_queryset = Movie.objects.all()

	if search_query:
		movies = movie_queryset.filter(title__icontains=search_query)
		result_message = f'Search results for "{search_query}".'
		if not movies.exists():
			result_message = f'No movies found with "{search_query}".'
	elif show_all:
		movies = movie_queryset
		result_message = "Showing all movies."
	else:
		movies = movie_queryset.none()
		result_message = "Use search or click All movies to browse the full list."

	return render(
		request,
		"movies/list.html",
		{
			"movies": movies,
			"search_query": search_query,
			"result_message": result_message,
			"show_all": show_all,
		},
	)


@login_required
@require_POST
def add_to_watched_movies(request):
	movie_id = request.POST.get("movie_id")
	if not movie_id:
		return HttpResponseBadRequest("Missing movie id.")

	movie = get_object_or_404(Movie, id=movie_id)
	WatchedMovie.objects.get_or_create(
		user=request.user,
		title=movie.title,
		year=movie.year,
	)

	return redirect("movie-list")


@login_required
def profile(request):
	return render(request, "profile.html")


@login_required
def watched_movies_page(request):
	watched_movies = WatchedMovie.objects.filter(user=request.user)
	return render(request, "profile/watched_movies.html", {"watched_movies": watched_movies})


@login_required
def user_reviews_page(request):
	reviews = MovieReview.objects.filter(watched_movie__user=request.user).select_related("watched_movie")
	return render(request, "profile/user_reviews.html", {"reviews": reviews})


@login_required
def leave_review(request, watched_movie_id):
	watched_movie = get_object_or_404(WatchedMovie, id=watched_movie_id, user=request.user)

	try:
		review = watched_movie.review
	except MovieReview.DoesNotExist:
		review = None

	if request.method == "POST":
		form = MovieReviewForm(request.POST, instance=review)
		if form.is_valid():
			review_obj = form.save(commit=False)
			review_obj.watched_movie = watched_movie
			review_obj.save()
			return redirect("profile")
	else:
		form = MovieReviewForm(instance=review)

	context = {
		"watched_movie": watched_movie,
		"form": form,
	}
	return render(request, "movies/leave_review.html", context)


@login_required
def edit_review(request, review_id):
	# A01 Broken Access Control demo:
	# To make the fix active, comment this and uncomment the fix below.
	review = get_object_or_404(MovieReview, id=review_id)
	watched_movie = review.watched_movie

	# Fix for A01 Broken Access Control:
	#review = get_object_or_404(MovieReview, id=review_id)
	#watched_movie = review.watched_movie
	#if watched_movie.user != request.user:
	#	return HttpResponseForbidden("You are not allowed to edit this review.")

	if request.method == "POST":
		form = MovieReviewForm(request.POST, instance=review)
		if form.is_valid():
			form.save()
			return redirect("profile")
	else:
		form = MovieReviewForm(instance=review)

	context = {
		"watched_movie": watched_movie,
		"form": form,
		"review": review,
	}
	return render(request, "movies/leave_review.html", context)


def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("home")
	else:
		form = UserCreationForm()

	return render(request, "registration/register.html", {"form": form})


def login_view(request):
	if request.method == "POST":
		form = ShortAuthenticationForm(request, data=request.POST)
		username = request.POST.get("username", "").strip()
		password = request.POST.get("password", "")

		# A07 Identification and Authentication Failures:
		# To make the fix active, comment this and uncomment the fix.
		user = get_object_or_404(User, username=username)
		login(request, user)
		return redirect("home")

		# Fix for A07 Identification and Authentication Failures:
		#user = authenticate(request, username=username, password=password)
		#if user is not None:
		#	login(request, user)
		#	return redirect("home")

	else:
		form = ShortAuthenticationForm(request)

	return render(request, "registration/login.html", {"form": form})


logout_view = LogoutView.as_view(next_page="login")
