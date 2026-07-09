from django.urls import path
from .views import ProductDetailView, SellerDashboardView

# KITA HAPUS app_name = 'products' agar semua template lama (Homepage/Header) tidak rusak

urlpatterns = [
    # Rute untuk Detail Produk (Bawaan proyek Anda) - Diakses via {% url 'product_detail' product.id %}
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    
    # Rute untuk Dashboard Penjual (STEP 15) - Diakses via {% url 'seller_dashboard' %}
    path('dashboard/', SellerDashboardView.as_view(), name='seller_dashboard'),
]