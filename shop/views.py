from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .models import Order

@staff_member_required
def admin_order_list(request):
    # تست موقت برای بررسی اینکه آیا صفحه ادمین بالا می‌آید یا خیر
    return HttpResponse("Test Admin Orders Page works!")
    
    # کد اصلی شما (بعد از تست این را از حالت کامنت خارج می‌کنیم):
    # orders = Order.objects.all()
    # return render(request, 'shop/admin/order_list.html', {'orders': orders})
