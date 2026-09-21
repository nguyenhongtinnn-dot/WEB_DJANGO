from django import forms
from django.core.exceptions import ValidationError

from .models import Book, Publisher, Review


def validate_rating(value):
    if value < 0 or value > 5:
        raise ValidationError("Điểm đánh giá phải từ 0 đến 5.")


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        min_length=3,
        label="Tìm sách",
        widget=forms.TextInput(
            attrs={"placeholder": "Nhập ít nhất 3 ký tự...", "class": "input"}
        ),
    )
    search_in = forms.ChoiceField(
        required=False,
        label="Tìm trong",
        choices=(("title", "Tiêu đề"), ("contributor", "Tác giả")),
        widget=forms.Select(attrs={"class": "input"}),
    )


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ["name", "website", "email"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input"}),
            "website": forms.URLInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
        }


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=0,
        max_value=5,
        validators=[validate_rating],
        widget=forms.NumberInput(attrs={"class": "input", "min": 0, "max": 5}),
        label="Điểm (0-5)",
    )

    class Meta:
        model = Review
        fields = ["content", "rating"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "input", "rows": 6}),
        }


class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["cover", "sample"]
        widgets = {
            "cover": forms.ClearableFileInput(attrs={"class": "input"}),
            "sample": forms.ClearableFileInput(attrs={"class": "input"}),
        }
