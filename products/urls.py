from django.urls import path
from .views import (
    HomeView,  # Pastikan HomeView di-import di sini
    ProductDetailView, 
    SellerDashboardView, 
    ProductCreateView, 
    ProductUpdateView, 
    ProductDeleteView,
    seller_profile_view
)

urlpatterns = [
    # Jalur Beranda Utama menggunakan HomeView
    path('', HomeView.as_view(), name='home'),
    
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('dashboard/', SellerDashboardView.as_view(), name='seller_dashboard'),
    path('add/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    
    # Rute Profil Publik Penjual
    path('seller/<str:username>/', seller_profile_view, name='seller_profile'),
]