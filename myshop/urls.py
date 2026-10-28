from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # این خط را اضافه کنید تا صفحات لاگین و لاگ‌اوت جنگو کار کنند
    path('accounts/', include('django.contrib.auth.urls')), 
    
    path('', include('shop.urls')),
]