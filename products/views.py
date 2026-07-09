from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product

# 1. VIEW DETAIL PRODUK
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'  # Mengarah ke templates/products/product_detail.html
    context_object_name = 'product'


# 2. VIEW DASHBOARD PENJUAL
class SellerDashboardView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/seller_dashboard.html'  # Mengarah ke templates/products/seller_dashboard.html
    context_object_name = 'my_products'

    def get_queryset(self):
        # Mengambil produk khusus milik user yang sedang login
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')