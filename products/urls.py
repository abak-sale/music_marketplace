from django.urls import path
from .views import ProductDetailView, SellerDashboardView, ProductCreateView

urlpatterns = [
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('dashboard/', SellerDashboardView.as_view(), name='seller_dashboard'),
    
    # Rute Baru untuk Tambah Produk
    path('add/', ProductCreateView.as_view(), name='product_create'),
]