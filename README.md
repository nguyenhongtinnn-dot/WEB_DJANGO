# Bookr — website đánh giá sách (Django, chương 1–10)

Project theo lộ trình tài liệu Web Django đến **chương 10**. Chưa cấu hình Git/GitHub và Render (bạn tự làm phần đó).

## Nội dung đã làm

| Chương | Nội dung |
|--------|----------|
| 1 | Project Django `bookr`, app `reviews` |
| 2 | Model & migration: Publisher, Book, Contributor, BookContributor, Review |
| 3 | Views, URL, template: danh sách sách, chi tiết, tìm kiếm |
| 4 | Django Admin đăng ký model, filter, search, inline |
| 5 | Static files (`static/css/bookr.css`) |
| 6–7 | Form tìm kiếm, ModelForm đánh giá/NXB, validate điểm 0–5 |
| 8 | Upload ảnh bìa và file mẫu (`MEDIA`) |
| 9 | Session, đăng nhập/đăng xuất, `@login_required` |
| 10 | Custom AdminSite, template logout, dashboard tìm kiếm |

## Chạy local

```powershell
cd e:\CNLTHD_Web
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

Mở http://127.0.0.1:8000/

- Superuser: `admin` / `admin123`
- User thường: `reader` / `reader123`
- Admin tùy chỉnh: http://127.0.0.1:8000/admin/
