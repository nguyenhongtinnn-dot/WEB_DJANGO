#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Xóa thư mục gom cũ nếu có và gom mới hoàn toàn
rm -rf staticfiles
python manage.py collectstatic --noinput --clear
python manage.py migrate

# Tự động nạp dữ liệu sách mẫu
python manage.py seed_data || true

# Tự động tạo tài khoản Admin (Nếu chưa có)
DJANGO_SUPERUSER_PASSWORD=Admin123456 python manage.py createsuperuser --noinput --username admin --email admin@gmail.com || true