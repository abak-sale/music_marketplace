from django.urls import path
from .views import (
    ProductDetailView, 
    SellerDashboardView, 
    ProductCreateView, 
    ProductUpdateView, 
    ProductDeleteView
)

urlpatterns = [
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('dashboard/', SellerDashboardView.as_view(), name='seller_dashboard'),
    path('add/', ProductCreateView.as_view(), name='product_create'),
    
    # Rute Baru Edit dan Hapus
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]