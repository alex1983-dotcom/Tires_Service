from django.urls import path
from .views import CategoryListView, ProductListView, CartDetailView, AddToCartView, CheckoutView, CategoryProductsView, OrderSuccessView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('categories/<int:category_id>/products/', CategoryProductsView.as_view(), name='category-products'),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('cart/add/<int:product_id>/', AddToCartView.as_view(), name='add-to-cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/success/<int:order_id>/', OrderSuccessView.as_view(), name='order-success'),
]
