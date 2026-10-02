from django.urls import path

from . import views
from .models import Book

app_name = "reviews"

urlpatterns = [
    path("", views.home, name="book_list"),
    path("movies/", views.film_list, {"kind": Book.Kind.MOVIE}, name="movies"),
    path("series/", views.film_list, {"kind": Book.Kind.SERIES}, name="series"),
    path("audio/", views.film_list, {"kind": Book.Kind.AUDIO}, name="audio"),
    path("books/", views.home, name="books"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("films/<int:pk>/", views.book_detail, name="film_detail"),
    path("books/<int:pk>/media/", views.book_media, name="book_media"),
    path("books/<int:book_pk>/review/", views.review_edit, name="review_create"),
    path(
        "books/<int:book_pk>/review/<int:review_pk>/",
        views.review_edit,
        name="review_edit",
    ),
    path("book-search/", views.book_search, name="book_search"),
    path("publishers/new/", views.publisher_edit, name="publisher_create"),
    path("publishers/<int:pk>/", views.publisher_edit, name="publisher_edit"),
]
