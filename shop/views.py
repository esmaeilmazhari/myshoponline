import random
import string
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .models import Product, Order, OrderItem
from .cart import Cart


# ========== محصولات ==========

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        
        # منطق جستجو
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(available=True)


# ========== سبد خرید ==========

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart/detail.html', {'cart': cart})


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if product.stock == 0:
        messages.error(request, f'محصول «{product.name}» موجود نیست.')
        return redirect('shop:cart_detail')
    
    if product.stock < quantity:
        messages.error(request, f'موجودی محصول «{product.name}» کافی نیست. (موجودی فعلی: {product.stock})')
        return redirect('shop:cart_detail')
    
    override = request.POST.get('override', False)
    cart.add(product=product, quantity=quantity, override_quantity=override)
    return redirect('shop:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('shop:cart_detail')


# ========== سفارش ==========

def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        
        if not first_name:
            messages.error(request, 'لطفاً فرم را به درستی پر کنید.')
            return redirect('shop:order_create')

        order = Order.objects.create(
            first_name=first_name,
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            postal_code=request.POST.get('postal_code'),
            phone=request.POST.get('phone'),
        )

        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
            )

        cart.clear()
        request.session['order_id'] = order.id

        return redirect('shop:payment_process', order_id=order.id)

    return render(request, 'shop/order/create.html', {'cart': cart})


# ========== پرداخت ==========

def payment_process(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        card_number = request.POST.get('card_number', '').replace('-', '').replace(' ', '')
        cvv2 = request.POST.get('cvv2', '')
        expiry_date = request.POST.get('expiry_date', '')

        if len(card_number) != 16 or not card_number.isdigit():
            messages.error(request, 'شماره کارت نامعتبر است. باید دقیقاً ۱۶ رقم باشد.')
            return render(request, 'shop/order/pay.html', {'order': order})

        if len(cvv2) < 3 or not cvv2.isdigit():
            messages.error(request, 'کد CVV2 نامعتبر است.')
            return render(request, 'shop/order/pay.html', {'order': order})

        if not expiry_date:
            messages.error(request, 'تاریخ انقضا را وارد کنید.')
            return render(request, 'shop/order/pay.html', {'order': order})

        tracking_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        
        order.paid = True
        order.tracking_code = tracking_code
        order.save()

        for item in order.items.all():
            item.product.stock -= item.quantity
            item.product.save()

        return redirect('shop:payment_callback', order_id=order.id)

    return render(request, 'shop/order/pay.html', {'order': order})


def payment_callback(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order/payment_success.html', {'order': order})


# ========== مدیریت سفارشات ==========

@staff_member_required
def admin_order_list(request):
    orders = Order.objects.order_by('-created')
    return render(request, 'shop/admin/order_list.html', {'orders': orders})


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/admin/order_detail.html', {'order': order})


@staff_member_required
def admin_order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        if order.paid:
            for item in order.items.all():
                item.product.stock += item.quantity
                item.product.save()
        
        order.delete()
        
        messages.success(request, f'سفارش #{order_id} با موفقیت حذف شد و موجودی محصولات به انبار برگشت.')
        return redirect('shop:admin_order_list')
        
    return redirect('shop:admin_order_list')