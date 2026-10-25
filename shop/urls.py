from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),

    # سبد خرید
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),

    # سفارش و پرداخت
    path('order/', views.order_create, name='order_create'),
    path('order/<int:order_id>/pay/', views.payment_process, name='payment_process'),
    path('order/<int:order_id>/callback/', views.payment_callback, name='payment_callback'),

    # پنل ادمین سفارشات
    path('admin-orders/', views.admin_order_list, name='admin_order_list'),
    path('admin-orders/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-orders/<int:order_id>/delete/', views.admin_order_delete, name='admin_order_delete'),

    # جزئیات محصول (باید آخر باشد)
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]