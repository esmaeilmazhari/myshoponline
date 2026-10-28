from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .models import Order, Product

def product_list(request):
    products = Product.objects.filter(available=True)
    return render(request, 'shop/product/list.html', {
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})

@staff_member_required
def admin_order_list(request):
    # تست موقت ادمین
    return HttpResponse("Test Admin Orders Page works!")
    
    # بعد از تایید، به این شکل تغییر می‌کند:
    # orders = Order.objects.all()
    # return render(request, 'shop/admin/order_list.html', {'orders': orders})
