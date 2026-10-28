from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from .models import Order, Product, Category

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/product/detail.html', {'product': product})

@staff_member_required
def admin_order_list(request):
    # برای پیدا کردن خطای 500، فعلاً این خط فعال است تا متن زیر چاپ شود:
    return HttpResponse("Test Admin Orders Page works!")
    
    # بعد از اینکه مطمئن شدیم صفحه بالا می‌آید، این بخش را جایگزین می‌کنیم:
    # orders = Order.objects.all()
    # return render(request, 'shop/admin/order_list.html', {'orders': orders})
