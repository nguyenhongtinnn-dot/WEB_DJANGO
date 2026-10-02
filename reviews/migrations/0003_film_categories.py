from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reviews", "0002_book_content_book_sample_video_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="kind",
            field=models.CharField(
                choices=[
                    ("movie", "Phim movie"),
                    ("series", "Phim series"),
                    ("audio", "Phim audio"),
                ],
                db_index=True,
                default="movie",
                max_length=20,
                verbose_name="Loại phim",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="episode_count",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Dùng cho phim series hoặc audio nhiều tập.",
                null=True,
                verbose_name="Số tập",
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="duration_minutes",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Thời lượng (phút)"
            ),
        ),
        migrations.AlterField(
            model_name="publisher",
            name="name",
            field=models.CharField(max_length=80, verbose_name="Tên hãng phim"),
        ),
        migrations.AlterField(
            model_name="book",
            name="title",
            field=models.CharField(max_length=120, verbose_name="Tên phim"),
        ),
        migrations.AlterField(
            model_name="book",
            name="isbn",
            field=models.CharField(max_length=20, unique=True, verbose_name="Mã phim"),
        ),
        migrations.AlterField(
            model_name="bookcontributor",
            name="role",
            field=models.CharField(
                choices=[
                    ("DIRECTOR", "Đạo diễn"),
                    ("ACTOR", "Diễn viên"),
                    ("WRITER", "Biên kịch"),
                    ("AUTHOR", "Tác giả"),
                    ("CO_AUTHOR", "Đồng tác giả"),
                    ("EDITOR", "Biên tập"),
                ],
                max_length=20,
                verbose_name="Vai trò",
            ),
        ),
    ]
