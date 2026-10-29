from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView
from .cart import Cart
from .forms import CartAddProductForm
from .models import Category, Order, OrderItem, Product
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test


class ProductListView(ListView):
  model = Product
  template_name = (
      'shop/product_list.html'  # هماهنگ با فایل موجود در پروژه شما
  )
  context_object_name = 'products'

  def get_queryset(self):
    queryset = super().get_queryset()
    category_slug = self.kwargs.get('category_slug')
    if category_slug:
      self.category = get_object_or_404(Category, slug=category_slug)
      queryset = queryset.filter(category=self.category)
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['categories'] = Category.objects.all()
    if hasattr(self, 'category'):
      context['current_category'] = self.category
    return context


class ProductDetailView(DetailView):
  model = Product
  template_name = (
      'shop/product_detail.html'  # هماهنگ با فایل موجود در پروژه شما
  )
  context_object_name = 'product'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['cart_product_form'] = CartAddProductForm()
    return context


def cart_detail(request):
  cart = Cart(request)
  for item in cart:
    item['update_quantity_form'] = CartAddProductForm(
        initial={'quantity': item['quantity'], 'override': True}
    )
  return render(request, 'shop/cart/cart_detail.html', {'cart': cart})


def cart_add(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(Product, id=product_id)
  form = CartAddProductForm(request.POST)
  if form.is_valid():
    cd = form.cleaned_data
    cart.add(
        product=product, quantity=cd['quantity'], override_quantity=cd['override']
    )
  return redirect('shop:cart_detail')


def cart_remove(request, product_id):
  cart = Cart(request)
  product = get_object_or_404(Product, id=product_id)
  cart.remove(product)
  return redirect('shop:cart_detail')


def order_create(request):
  cart = Cart(request)
  if request.method == 'POST':
    # دریافت اطلاعات ارسال شده از کاربر (در صورت وجود فرم ثبت سفارش)
    order = Order.objects.create()
    for item in cart:
      OrderItem.objects.create(
          order=order,
          product=item['product'],
          price=item['price'],
          quantity=item['quantity'],
      )
    cart.clear()
    return render(request, 'shop/order/created.html', {'order': order})
  return render(request, 'shop/order/order_create.html', {'cart': cart})


def payment_process(request):
  # منطق اتصال به درگاه پرداخت
  return render(request, 'shop/payment_process.html')


def payment_callback(request):
  # منطق بازگشت از درگاه پرداخت
  return render(request, 'shop/payment_callback.html')


@user_passes_test(lambda u: u.is_staff)
def admin_order_list(request):
  orders = Order.objects.all().order_by(
      '-created_at' if hasattr(Order, 'created_at') else '-id'
  )
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
