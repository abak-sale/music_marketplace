from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm

# 1. VIEW DETAIL PRODUK
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


# 2. VIEW DASHBOARD PENJUAL
class SellerDashboardView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/seller_dashboard.html'
    context_object_name = 'my_products'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')


# 3. VIEW TAMBAH PRODUK BARU (STEP 16)
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('seller_dashboard') # Jika sukses, kembali ke dashboard

    def form_valid(self, form):
        # Otomatis mengikat field 'seller' ke user yang sedang login saat ini
        form.instance.seller = self.request.user
        return super().form_valid(form)