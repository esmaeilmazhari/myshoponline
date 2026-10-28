from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from .models import Product, Order, OrderItem

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(pk=product_id)
            total_price += product.price * quantity
            cart_items.append({
                'product': product, 
                'quantity': quantity, 
                'total_price': product.price * quantity
            })
        except Product.DoesNotExist:
            continue
            
    return render(request, 'shop/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    
    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1
        
    request.session['cart'] = cart
    return redirect('cart_detail')

@user_passes_test(lambda u: u.is_staff)
def app_admin_order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'shop/admin/order_list.html', {'orders': orders})
