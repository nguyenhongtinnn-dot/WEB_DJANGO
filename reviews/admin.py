from django.contrib import admin

from .models import Book, BookContributor, Contributor, Publisher, Review


class BookContributorInline(admin.TabularInline):
    model = BookContributor
    extra = 1


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    readonly_fields = ("date_created", "date_edited")


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "email")
    search_fields = ("name", "email")


@admin.register(Contributor)
class ContributorAdmin(admin.ModelAdmin):
    list_display = ("first_names", "last_names", "email")
    search_fields = ("first_names", "last_names", "email")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "isbn", "publication_date", "publisher")
    list_filter = ("publisher", "publication_date")
    search_fields = ("title", "isbn")
    date_hierarchy = "publication_date"
    inlines = [BookContributorInline, ReviewInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "rating", "creator", "date_created")
    list_filter = ("rating", "date_created")
    search_fields = ("content", "book__title", "creator__username")
