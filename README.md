# Movie Review

Basic Django web application for managing and reviewing watched movies.  

Project was created for the Cyber Security Base MOOC course project at the University of Helsinki. The purpose of the application is to demonstrate security vulnerabilities listed on the OWASP top 10 and present possible fixes for them.

## Features
- user registration and log in   
- public movie listing
- public review listing
- search movies by title
- search users
- personal "Watched movies" page for users to manage their watched movies
- personal "Your reviews" page for users to manage their reviews
- add and review watched movies

## Getting started


1. Clone the repository.  
```git clone https://github.com/ilkkaluu/Movie-Review.git```
```cd Movie-Review```
3. Create and activate a virtual environment.   
```python3 -m venv venv```   
```source venv/bin/activate```
5. Install dependencies with `pip install -r requirements.txt`.
6. Run migrations with `python manage.py migrate`.
7. Start the development server with `python manage.py runserver`.
8. Open your browser and visit `http://127.0.0.1:8000/`.

## Authentication

- Register a new user at `http://127.0.0.1:8000/register/`.
- Log in at `http://127.0.0.1:8000/login/`.
- Log out from the navigation link after signing in.

## Optional admin access

1. Create a superuser with `python manage.py createsuperuser`.
2. Open `http://127.0.0.1:8000/admin/` and log in with the superuser account.
3. In admin you can:
	- add/remove movies from the `Movies` section
	- remove users' watched movies from `Watched movies`
	- remove users' reviews from `Movie reviews`
