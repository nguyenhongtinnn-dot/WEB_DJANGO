# CineNoir — website đánh giá phim (Django, chương 1–10)

Website đổi từ Bookr (sách) sang thư viện phim với 3 mục: **Movie**, **Series**, **Audio**. Giao diện theme tối.

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
- Admin: http://127.0.0.1:8000/admin/

## Mục phim

- `/` trang chủ (3 kệ phim)
- `/movies/` phim movie
- `/series/` phim series nhiều tập
- `/audio/` phim audio
- `/book-search/` tìm kiếm theo tên / ekip / loại
