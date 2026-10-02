from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q

from .forms import BookMediaForm, PublisherForm, ReviewForm, SearchForm
from .models import Book, BookContributor, Contributor, Publisher, Review

KIND_META = {
    Book.Kind.MOVIE: {
        "title": "Phim movie",
        "subtitle": "Phim điện ảnh chiếu rạp và phim lẻ.",
    },
    Book.Kind.SERIES: {
        "title": "Phim series",
        "subtitle": "Phim nhiều tập — theo dõi từng mùa, từng tập.",
    },
    Book.Kind.AUDIO: {
        "title": "Phim audio",
        "subtitle": "Phim âm thanh, audio drama và truyện kể bằng lời.",
    },
}


def _film_queryset():
    return Book.objects.select_related("publisher").prefetch_related("contributors")


def home(request):
    films = _film_queryset()
    return render(
        request,
        "reviews/home.html",
        {
            "movies": films.filter(kind=Book.Kind.MOVIE)[:8],
            "series": films.filter(kind=Book.Kind.SERIES)[:8],
            "audios": films.filter(kind=Book.Kind.AUDIO)[:8],
        },
    )


def film_list(request, kind):
    meta = KIND_META.get(kind)
    if not meta:
        return redirect("reviews:book_list")
    films = _film_queryset().filter(kind=kind)
    return render(
        request,
        "reviews/book_list.html",
        {
            "books": films,
            "kind": kind,
            "page_title": meta["title"],
            "page_subtitle": meta["subtitle"],
        },
    )


def book_list(request):
    return home(request)


def book_detail(request, pk):
    book = get_object_or_404(_film_queryset(), pk=pk)
    reviews = book.review_set.select_related("creator")
    roles = BookContributor.objects.filter(book=book).select_related("contributor")
    return render(
        request,
        "reviews/book_detail.html",
        {"book": book, "reviews": reviews, "roles": roles},
    )


def book_search(request):
    form = SearchForm(request.GET or None)
    books = Book.objects.none()
    searched = False

    if form.is_valid():
        search = (form.cleaned_data.get("search") or "").strip()
        search_in = form.cleaned_data.get("search_in") or "title"
        kind = form.cleaned_data.get("kind") or ""
        if search:
            searched = True
            if search_in == "contributor":
                contributors = Contributor.objects.filter(
                    Q(first_names__icontains=search) | Q(last_names__icontains=search)
                )
                books = Book.objects.filter(contributors__in=contributors).distinct()
            else:
                books = Book.objects.filter(
                    Q(title__icontains=search) | Q(content__icontains=search)
                )
            if kind:
                books = books.filter(kind=kind)
            books = books.select_related("publisher")

    return render(
        request,
        "reviews/book_search.html",
        {"form": form, "books": books, "searched": searched},
    )


@login_required
def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    instance = None
    if review_pk is not None:
        instance = get_object_or_404(Review, pk=review_pk, book=book)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=instance)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.creator = request.user
            if instance is not None:
                review.date_edited = timezone.now()
            review.save()
            return redirect("reviews:book_detail", pk=book.pk)
    else:
        form = ReviewForm(instance=instance)

    return render(
        request,
        "reviews/review_form.html",
        {"form": form, "book": book, "instance": instance},
    )


@login_required
def publisher_edit(request, pk=None):
    instance = get_object_or_404(Publisher, pk=pk) if pk else None
    if request.method == "POST":
        form = PublisherForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("reviews:book_list")
    else:
        form = PublisherForm(instance=instance)
    return render(
        request,
        "reviews/publisher_form.html",
        {"form": form, "instance": instance},
    )


@login_required
def book_media(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect("reviews:book_detail", pk=book.pk)
    else:
        form = BookMediaForm(instance=book)
    return render(request, "reviews/book_media.html", {"form": form, "book": book})
