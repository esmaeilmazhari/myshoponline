from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView
from .models import Product, Order, OrderItem

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

# --- سبد خرید ---
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
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        
    return redirect('shop:cart_detail')

def cart_clear(request):
    if 'cart' in request.session:
        del request.session['cart']
    return redirect('shop:cart_detail')

# --- سفارش و پرداخت ---
def order_create(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('shop:cart_detail')
    
    if request.method == 'POST':
        # ایجاد سفارش ساده
        order = Order.objects.create() # فیلدهای سفارشی بسته به مدل شما
        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            OrderItem.objects.create(order=order, product=product, price=product.price, quantity=quantity)
        
        # پاک کردن سبد خرید بعد از ثبت سفارش
        del request.session['cart']
        return redirect('shop:payment_process', order_id=order.id)
        
    return render(request, 'shop/order_create.html')

def payment_process(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'shop/payment_process.html', {'order': order})

def payment_callback(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'shop/payment_callback.html', {'order': order})

# --- پنل ادمین سفارشات ---
@user_passes_test(lambda u: u.is_staff)
def admin_order_list(request):
    orders = Order.objects.all().order_by('-created_at') if hasattr(Order, 'created_at') else Order.objects.all()
    return render(request, 'shop/admin/order_list.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, 'shop/admin/order_detail.html', {'order': order})

@user_passes_test(lambda u: u.is_staff)
def admin_order_delete(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    return redirect('shop:admin_order_list')
