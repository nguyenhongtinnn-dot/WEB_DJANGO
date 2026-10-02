from django import forms
from django.core.exceptions import ValidationError

from .models import Book, Publisher, Review


def validate_rating(value):
    if value < 0 or value > 5:
        raise ValidationError("Điểm đánh giá phải từ 0 đến 5.")


INPUT = {"class": "input"}


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        min_length=2,
        label="Tìm phim",
        widget=forms.TextInput(
            attrs={**INPUT, "placeholder": "Tên phim, đạo diễn, diễn viên..."}
        ),
    )
    search_in = forms.ChoiceField(
        required=False,
        label="Tìm trong",
        choices=(
            ("title", "Tên phim"),
            ("contributor", "Đạo diễn / diễn viên"),
        ),
        widget=forms.Select(attrs=INPUT),
    )
    kind = forms.ChoiceField(
        required=False,
        label="Loại phim",
        choices=(
            ("", "Tất cả"),
            (Book.Kind.MOVIE, "Phim movie"),
            (Book.Kind.SERIES, "Phim series"),
            (Book.Kind.AUDIO, "Phim audio"),
        ),
        widget=forms.Select(attrs=INPUT),
    )


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ["name", "website", "email"]
        widgets = {
            "name": forms.TextInput(attrs=INPUT),
            "website": forms.URLInput(attrs=INPUT),
            "email": forms.EmailInput(attrs=INPUT),
        }


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=0,
        max_value=5,
        validators=[validate_rating],
        widget=forms.NumberInput(attrs={**INPUT, "min": 0, "max": 5}),
        label="Điểm (0-5)",
    )

    class Meta:
        model = Review
        fields = ["content", "rating"]
        widgets = {
            "content": forms.Textarea(
                attrs={**INPUT, "rows": 6, "placeholder": "Cảm nhận của bạn về bộ phim..."}
            ),
        }


class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["cover", "sample", "sample_video_url", "content"]
        widgets = {
            "cover": forms.ClearableFileInput(attrs=INPUT),
            "sample": forms.ClearableFileInput(attrs=INPUT),
            "sample_video_url": forms.TextInput(
                attrs={**INPUT, "placeholder": "https://www.youtube.com/watch?v=..."}
            ),
            "content": forms.Textarea(attrs={**INPUT, "rows": 6}),
        }
