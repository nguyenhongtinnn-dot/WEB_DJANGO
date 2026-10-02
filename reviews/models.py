from django.contrib.auth.models import User
from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=80, verbose_name="Tên hãng phim")
    website = models.URLField(verbose_name="Website")
    email = models.EmailField(verbose_name="Email")

    class Meta:
        verbose_name = "Hãng phim"
        verbose_name_plural = "Hãng phim"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Contributor(models.Model):
    first_names = models.CharField(max_length=50, verbose_name="Tên")
    last_names = models.CharField(max_length=50, verbose_name="Họ")
    email = models.EmailField(verbose_name="Email")

    class Meta:
        verbose_name = "Thành viên ekip"
        verbose_name_plural = "Thành viên ekip"
        ordering = ["last_names", "first_names"]

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_names} {self.last_names}"

    def initials(self):
        first = "".join(part[0] for part in self.first_names.split() if part)
        last = "".join(part[0] for part in self.last_names.split() if part)
        return f"{first}{last}".upper()


class Book(models.Model):
    class Kind(models.TextChoices):
        MOVIE = "movie", "Phim movie"
        SERIES = "series", "Phim series"
        AUDIO = "audio", "Phim audio"

    title = models.CharField(max_length=120, verbose_name="Tên phim")
    publication_date = models.DateField(verbose_name="Ngày phát hành")
    isbn = models.CharField(max_length=20, unique=True, verbose_name="Mã phim")
    kind = models.CharField(
        max_length=20,
        choices=Kind.choices,
        default=Kind.MOVIE,
        verbose_name="Loại phim",
        db_index=True,
    )
    episode_count = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Số tập",
        help_text="Dùng cho phim series hoặc audio nhiều tập.",
    )
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Thời lượng (phút)",
    )
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, verbose_name="Hãng phim"
    )
    contributors = models.ManyToManyField(
        Contributor, through="BookContributor", verbose_name="Ekip"
    )
    cover = models.ImageField(
        upload_to="book_covers/", blank=True, verbose_name="Poster"
    )
    sample = models.FileField(
        upload_to="book_samples/", blank=True, verbose_name="File audio / mẫu"
    )
    content = models.TextField(blank=True, null=True, verbose_name="Nội dung / tóm tắt")
    sample_video_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Trailer / video (URL YouTube hoặc file)",
    )

    class Meta:
        verbose_name = "Phim"
        verbose_name_plural = "Phim"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.get_kind_display()})"

    def isbn10(self):
        digits = "".join(ch for ch in self.isbn if ch.isdigit() or ch.upper() == "X")
        if len(digits) == 10:
            return digits
        if len(digits) == 13 and digits.startswith("978"):
            core = digits[3:12]
            total = sum((i + 1) * int(d) for i, d in enumerate(core))
            check = total % 11
            check_char = "X" if check == 10 else str(check)
            return core + check_char
        return self.isbn

    def average_rating(self):
        ratings = list(self.review_set.values_list("rating", flat=True))
        if not ratings:
            return None
        return round(sum(ratings) / len(ratings), 1)

    def trailer_src(self):
        value = self.sample_video_url
        if not value:
            return ""
        if hasattr(value, "url"):
            return value.url or ""
        return str(value)

    def youtube_embed_url(self):
        url = self.trailer_src()
        if not url:
            return ""
        if "youtube.com/embed/" in url:
            return url
        if "youtube.com/watch" in url and "v=" in url:
            video_id = url.split("v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return ""

    def is_audio(self):
        return self.kind == self.Kind.AUDIO

    def is_series(self):
        return self.kind == self.Kind.SERIES


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        DIRECTOR = "DIRECTOR", "Đạo diễn"
        ACTOR = "ACTOR", "Diễn viên"
        WRITER = "WRITER", "Biên kịch"
        AUTHOR = "AUTHOR", "Tác giả"
        CO_AUTHOR = "CO_AUTHOR", "Đồng tác giả"
        EDITOR = "EDITOR", "Biên tập"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20, choices=ContributionRole.choices, verbose_name="Vai trò"
    )

    class Meta:
        verbose_name = "Vai trò ekip"
        verbose_name_plural = "Vai trò ekip"
        unique_together = ("book", "contributor", "role")

    def __str__(self):
        return f"{self.contributor} — {self.get_role_display()} — {self.book.title}"


class Review(models.Model):
    content = models.TextField(help_text="Nội dung đánh giá", verbose_name="Nội dung")
    rating = models.IntegerField(help_text="Điểm từ 0 đến 5", verbose_name="Điểm")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    date_edited = models.DateTimeField(null=True, blank=True, verbose_name="Ngày sửa")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Người viết"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Phim")

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.book.title} — {self.rating}/5"
