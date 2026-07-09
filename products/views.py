from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
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


# 3. VIEW TAMBAH PRODUK BARU
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('seller_dashboard')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


# 4. VIEW UBAH PRODUK (STEP 17)
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'  # Memakai template yang sama dengan Create agar hemat file
    success_url = reverse_lazy('seller_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Sistem Keamanan: Memastikan orang lain tidak bisa mengedit produk milik Anda lewat URL
        if obj.seller != self.request.user:
            raise PermissionDenied("Anda tidak memiliki hak untuk mengubah produk ini.")
        return obj


# 5. VIEW HAPUS PRODUK (STEP 17)
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('seller_dashboard')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Sistem Keamanan: Memastikan orang lain tidak bisa menghapus produk milik Anda
        if obj.seller != self.request.user:
            raise PermissionDenied("Anda tidak memiliki hak untuk menghapus produk ini.")
        return obj