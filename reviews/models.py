from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField  # Import CloudinaryField


class Publisher(models.Model):
    name = models.CharField(max_length=50, verbose_name="Tên nhà xuất bản")
    website = models.URLField(verbose_name="Website")
    email = models.EmailField(verbose_name="Email")

    class Meta:
        verbose_name = "Nhà xuất bản"
        verbose_name_plural = "Nhà xuất bản"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Contributor(models.Model):
    first_names = models.CharField(max_length=50, verbose_name="Tên")
    last_names = models.CharField(max_length=50, verbose_name="Họ")
    email = models.EmailField(verbose_name="Email")

    class Meta:
        verbose_name = "Cộng tác viên"
        verbose_name_plural = "Cộng tác viên"
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
    title = models.CharField(max_length=70, verbose_name="Tiêu đề")
    publication_date = models.DateField(verbose_name="Ngày xuất bản")
    isbn = models.CharField(max_length=20, unique=True, verbose_name="ISBN")
    publisher = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, verbose_name="Nhà xuất bản"
    )
    contributors = models.ManyToManyField(
        Contributor, through="BookContributor", verbose_name="Cộng tác viên"
    )
    cover = models.ImageField(
        upload_to="book_covers/", blank=True, verbose_name="Ảnh bìa"
    )
    sample = models.FileField(
        upload_to="book_samples/", blank=True, verbose_name="Bản mẫu"
    )

    content = models.TextField(blank=True, null=True, verbose_name="Nội dung chi tiết")
    
    # --- ĐÃ ĐỔI TỪ CharField SANG CloudinaryField LỜI GIẢI CHO VIDEO ---
    sample_video_url = CloudinaryField(
        verbose_name="Video giới thiệu",
        resource_type="video",
        folder="book_videos/",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Sách"
        verbose_name_plural = "Sách"
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} ({self.isbn})"

    def isbn10(self):
        """Chuyển ISBN-13 (978...) sang ISBN-10 khi có thể."""
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
        ratings = self.review_set.values_list("rating", flat=True)
        if not ratings:
            return None
        return round(sum(ratings) / len(ratings), 1)


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Tác giả"
        CO_AUTHOR = "CO_AUTHOR", "Đồng tác giả"
        EDITOR = "EDITOR", "Biên tập"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20, choices=ContributionRole.choices, verbose_name="Vai trò"
    )

    class Meta:
        verbose_name = "Vai trò cộng tác"
        verbose_name_plural = "Vai trò cộng tác"
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
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Sách")

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.book.title} — {self.rating}/5"