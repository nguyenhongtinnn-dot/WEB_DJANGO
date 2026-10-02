from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from reviews.models import Book, BookContributor, Contributor, Publisher, Review


class Command(BaseCommand):
    help = "Tạo dữ liệu mẫu cho website phim"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@cinenoir.local", "admin123")
            self.stdout.write(self.style.SUCCESS("Đã tạo superuser admin / admin123"))

        viewer, _ = User.objects.get_or_create(
            username="reader",
            defaults={"email": "viewer@cinenoir.local"},
        )
        viewer.set_password("reader123")
        viewer.save()

        studios = {
            "warner": Publisher.objects.get_or_create(
                name="Warner Bros.",
                defaults={"website": "https://www.warnerbros.com", "email": "contact@warnerbros.com"},
            )[0],
            "netflix": Publisher.objects.get_or_create(
                name="Netflix",
                defaults={"website": "https://www.netflix.com", "email": "press@netflix.com"},
            )[0],
            "bhd": Publisher.objects.get_or_create(
                name="BHD / Galaxy Studio",
                defaults={"website": "https://www.bhdstar.vn", "email": "info@bhdstar.vn"},
            )[0],
            "bbc": Publisher.objects.get_or_create(
                name="BBC Audio",
                defaults={"website": "https://www.bbc.co.uk", "email": "audio@bbc.co.uk"},
            )[0],
        }

        people = {
            "villeneuve": Contributor.objects.get_or_create(
                email="denis@example.com",
                defaults={"first_names": "Denis", "last_names": "Villeneuve"},
            )[0],
            "bong": Contributor.objects.get_or_create(
                email="bong@example.com",
                defaults={"first_names": "Joon-ho", "last_names": "Bong"},
            )[0],
            "vu": Contributor.objects.get_or_create(
                email="tranthanhtam@example.com",
                defaults={"first_names": "Thành", "last_names": "Trấn"},
            )[0],
            "duffer": Contributor.objects.get_or_create(
                email="duffer@example.com",
                defaults={"first_names": "Matt", "last_names": "Duffer"},
            )[0],
            "hwang": Contributor.objects.get_or_create(
                email="hwang@example.com",
                defaults={"first_names": "Dong-hyuk", "last_names": "Hwang"},
            )[0],
            "orwell": Contributor.objects.get_or_create(
                email="orwell@example.com",
                defaults={"first_names": "George", "last_names": "Orwell"},
            )[0],
            "wells": Contributor.objects.get_or_create(
                email="wells@example.com",
                defaults={"first_names": "H. G.", "last_names": "Wells"},
            )[0],
            "nguyen": Contributor.objects.get_or_create(
                email="nguyentu@example.com",
                defaults={"first_names": "Tú", "last_names": "Nguyễn"},
            )[0],
        }

        films = [
            {
                "title": "Dune: Part Two",
                "isbn": "MOV-DUNE-2024",
                "kind": Book.Kind.MOVIE,
                "publication_date": date(2024, 3, 1),
                "publisher": studios["warner"],
                "duration_minutes": 166,
                "content": "Paul Atreides liên minh với người Fremen để trả thù và định đoạt số phận Arrakis.",
                "sample_video_url": "https://www.youtube.com/watch?v=Way9Dexny3w",
                "crew": [(people["villeneuve"], BookContributor.ContributionRole.DIRECTOR)],
            },
            {
                "title": "Parasite",
                "isbn": "MOV-PARA-2019",
                "kind": Book.Kind.MOVIE,
                "publication_date": date(2019, 5, 30),
                "publisher": studios["bhd"],
                "duration_minutes": 132,
                "content": "Hai gia đình đối lập giai cấp va chạm trong một ngôi nhà sang trọng ở Seoul.",
                "sample_video_url": "https://www.youtube.com/watch?v=5xH0HfJHsaY",
                "crew": [(people["bong"], BookContributor.ContributionRole.DIRECTOR)],
            },
            {
                "title": "Bố Già",
                "isbn": "MOV-BOGIA-2021",
                "kind": Book.Kind.MOVIE,
                "publication_date": date(2021, 3, 12),
                "publisher": studios["bhd"],
                "duration_minutes": 128,
                "content": "Câu chuyện gia đình Sài Gòn: tình cha con, mưu sinh và những lựa chọn khó khăn.",
                "crew": [(people["vu"], BookContributor.ContributionRole.DIRECTOR)],
            },
            {
                "title": "Stranger Things",
                "isbn": "SER-ST-2016",
                "kind": Book.Kind.SERIES,
                "publication_date": date(2016, 7, 15),
                "publisher": studios["netflix"],
                "episode_count": 34,
                "duration_minutes": 50,
                "content": "Nhóm bạn ở Hawkins đối mặt thế giới Upside Down và những bí ẩn siêu nhiên.",
                "sample_video_url": "https://www.youtube.com/watch?v=b9EkMcQRlbI",
                "crew": [(people["duffer"], BookContributor.ContributionRole.DIRECTOR)],
            },
            {
                "title": "Squid Game",
                "isbn": "SER-SG-2021",
                "kind": Book.Kind.SERIES,
                "publication_date": date(2021, 9, 17),
                "publisher": studios["netflix"],
                "episode_count": 9,
                "duration_minutes": 55,
                "content": "Người chơi phá sản tham gia trò chơi sinh tử để tranh giải thưởng khổng lồ.",
                "sample_video_url": "https://www.youtube.com/watch?v=oqxAJKy0ii4",
                "crew": [(people["hwang"], BookContributor.ContributionRole.WRITER)],
            },
            {
                "title": "The Bear",
                "isbn": "SER-BEAR-2022",
                "kind": Book.Kind.SERIES,
                "publication_date": date(2022, 6, 23),
                "publisher": studios["netflix"],
                "episode_count": 28,
                "duration_minutes": 30,
                "content": "Một đầu bếp fine-dining về điều hành tiệm sandwich của gia đình tại Chicago.",
                "crew": [(people["duffer"], BookContributor.ContributionRole.DIRECTOR)],
            },
            {
                "title": "The War of the Worlds (Audio)",
                "isbn": "AUD-WOW-1938",
                "kind": Book.Kind.AUDIO,
                "publication_date": date(1938, 10, 30),
                "publisher": studios["bbc"],
                "episode_count": 1,
                "duration_minutes": 60,
                "content": "Audio drama kinh điển về cuộc đổ bộ của sao Hỏa, kể bằng giọng tường thuật.",
                "crew": [(people["wells"], BookContributor.ContributionRole.AUTHOR)],
            },
            {
                "title": "1984 — Audio Drama",
                "isbn": "AUD-1984-2020",
                "kind": Book.Kind.AUDIO,
                "publication_date": date(2020, 4, 4),
                "publisher": studios["bbc"],
                "episode_count": 8,
                "duration_minutes": 45,
                "content": "Chuyển thể audio của 1984: Winston Smith sống dưới sự giám sát của Big Brother.",
                "crew": [(people["orwell"], BookContributor.ContributionRole.AUTHOR)],
            },
            {
                "title": "Đêm Sài Gòn — Audio",
                "isbn": "AUD-SG-2023",
                "kind": Book.Kind.AUDIO,
                "publication_date": date(2023, 8, 20),
                "publisher": studios["bhd"],
                "episode_count": 12,
                "duration_minutes": 25,
                "content": "Phim audio nhiều tập về những mảnh đời về đêm ở Sài Gòn.",
                "crew": [(people["nguyen"], BookContributor.ContributionRole.WRITER)],
            },
        ]

        for item in films:
            book, _created = Book.objects.update_or_create(
                isbn=item["isbn"],
                defaults={
                    "title": item["title"],
                    "kind": item["kind"],
                    "publication_date": item["publication_date"],
                    "publisher": item["publisher"],
                    "duration_minutes": item.get("duration_minutes"),
                    "episode_count": item.get("episode_count"),
                    "content": item.get("content", ""),
                    "sample_video_url": item.get("sample_video_url") or "",
                },
            )
            for person, role in item["crew"]:
                BookContributor.objects.get_or_create(
                    book=book, contributor=person, role=role
                )
            Review.objects.get_or_create(
                book=book,
                creator=viewer,
                defaults={
                    "content": f"{book.title} đáng xem trên CineNoir — {book.get_kind_display()}.",
                    "rating": 5,
                },
            )

        self.stdout.write(self.style.SUCCESS("Seeded film sample data."))
