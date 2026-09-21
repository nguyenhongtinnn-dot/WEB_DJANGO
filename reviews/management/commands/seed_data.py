from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import date

from reviews.models import Book, BookContributor, Contributor, Publisher, Review


class Command(BaseCommand):
    help = "Tạo dữ liệu mẫu Bookr (chương 1-10)"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@bookr.local", "admin123")
            self.stdout.write(self.style.SUCCESS("Đã tạo superuser admin / admin123"))

        reader, _ = User.objects.get_or_create(
            username="reader",
            defaults={"email": "reader@bookr.local"},
        )
        if not reader.has_usable_password():
            reader.set_password("reader123")
            reader.save()

        publishers = {
            "NXB Trẻ": Publisher.objects.get_or_create(
                name="NXB Trẻ",
                defaults={"website": "https://nxbtre.com.vn", "email": "info@nxbtre.com.vn"},
            )[0],
            "Packt": Publisher.objects.get_or_create(
                name="Packt Publishing",
                defaults={"website": "https://www.packtpub.com", "email": "info@packtpub.com"},
            )[0],
            "OReilly": Publisher.objects.get_or_create(
                name="O'Reilly Media",
                defaults={"website": "https://www.oreilly.com", "email": "info@oreilly.com"},
            )[0],
        }

        contributors = {
            "dung": Contributor.objects.get_or_create(
                email="tuan.dung@example.com",
                defaults={"first_names": "Tuấn Dũng", "last_names": "Trần"},
            )[0],
            "shaw": Contributor.objects.get_or_create(
                email="ben.shaw@example.com",
                defaults={"first_names": "Ben", "last_names": "Shaw"},
            )[0],
            "badhwar": Contributor.objects.get_or_create(
                email="saurabh.badhwar@example.com",
                defaults={"first_names": "Saurabh", "last_names": "Badhwar"},
            )[0],
            "holovaty": Contributor.objects.get_or_create(
                email="adrian@example.com",
                defaults={"first_names": "Adrian", "last_names": "Holovaty"},
            )[0],
        }

        books_data = [
            {
                "title": "Python & Django thực chiến",
                "isbn": "9786044797915",
                "publication_date": date(2024, 3, 1),
                "publisher": publishers["NXB Trẻ"],
                "authors": [contributors["dung"]],
            },
            {
                "title": "Web Development with Django",
                "isbn": "9781803230603",
                "publication_date": date(2023, 5, 26),
                "publisher": publishers["Packt"],
                "authors": [contributors["shaw"], contributors["badhwar"]],
            },
            {
                "title": "The Definitive Guide to Django",
                "isbn": "9781590597255",
                "publication_date": date(2009, 7, 1),
                "publisher": publishers["OReilly"],
                "authors": [contributors["holovaty"]],
            },
            {
                "title": "Two Scoops of Django",
                "isbn": "9780981467306",
                "publication_date": date(2022, 1, 15),
                "publisher": publishers["Packt"],
                "authors": [contributors["shaw"]],
            },
        ]

        for item in books_data:
            book, created = Book.objects.get_or_create(
                isbn=item["isbn"],
                defaults={
                    "title": item["title"],
                    "publication_date": item["publication_date"],
                    "publisher": item["publisher"],
                },
            )
            for index, author in enumerate(item["authors"]):
                role = (
                    BookContributor.ContributionRole.AUTHOR
                    if index == 0
                    else BookContributor.ContributionRole.CO_AUTHOR
                )
                BookContributor.objects.get_or_create(
                    book=book, contributor=author, defaults={"role": role}
                )

            if created or not book.review_set.exists():
                Review.objects.get_or_create(
                    book=book,
                    creator=reader,
                    defaults={
                        "content": f"Cuốn {book.title} rất hữu ích để học Django đến chương 10.",
                        "rating": 5,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Đã nạp dữ liệu mẫu."))
