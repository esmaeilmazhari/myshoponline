from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

# همیشه فایل‌های مدیا را سرو کن (حتی در حالت DEBUG=False برای پروژه روی Render)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
