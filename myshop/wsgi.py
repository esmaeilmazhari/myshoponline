"""
WSGI config for myshop project.
"""
import os
import cloudinary
from django.core.wsgi import get_wsgi_application

# اصلاح شد به myshop
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

# تنظیمات کلودینری برای آپلود عکس
cloudinary.config(
    cloud_name=os.environ.get('CLOUDINARY_CLOUD_NAME'),
    api_key=os.environ.get('CLOUDINARY_API_KEY'),
    api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
    secure=True
)

application = get_wsgi_application()