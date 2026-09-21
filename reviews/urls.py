from django.urls import path

from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.book_list, name="book_list"),
    path("books/", views.book_list, name="books"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
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
