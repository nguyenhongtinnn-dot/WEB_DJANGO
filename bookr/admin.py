from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path


class BookrAdminSite(admin.AdminSite):
    site_header = "Bookr administration"
    site_title = "Bookr Admin"
    index_title = "Bookr site admin"
    logout_template = "admin/logout.html"
    index_template = "admin/bookr_index.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "dashboard-search/",
                self.admin_view(self.dashboard_search),
                name="dashboard-search",
            ),
        ]
        return custom_urls + urls

    def dashboard_search(self, request):
        from reviews.models import Book, Contributor, Publisher, Review

        query = request.GET.get("q", "").strip()
        books = Book.objects.none()
        contributors = Contributor.objects.none()
        publishers = Publisher.objects.none()
        reviews = Review.objects.none()

        if query:
            books = Book.objects.filter(title__icontains=query)
            contributors = Contributor.objects.filter(
                first_names__icontains=query
            ) | Contributor.objects.filter(last_names__icontains=query)
            publishers = Publisher.objects.filter(name__icontains=query)
            reviews = Review.objects.filter(content__icontains=query)

        context = {
            **self.each_context(request),
            "title": "Tìm kiếm quản trị",
            "query": query,
            "books": books,
            "contributors": contributors,
            "publishers": publishers,
            "reviews": reviews,
        }
        return TemplateResponse(request, "admin/dashboard_search.html", context)

    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["dashboard_search_url"] = "admin:dashboard-search"
        return super().index(request, extra_context=extra_context)
