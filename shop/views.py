from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from .models import Product, Order, OrderItem

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

@user_passes_test(lambda u: u.is_staff)
app_admin_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'shop/admin/order_list.html', {'orders': orders})
