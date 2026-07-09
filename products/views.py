from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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


# 3. VIEW TAMBAH PRODUK BARU
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('seller_dashboard')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)


# 4. VIEW UBAH PRODUK - Menggunakan UserPassesTestMixin
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'  
    success_url = reverse_lazy('seller_dashboard')

    def test_func(self):
        # Mengambil data objek produk yang diakses
        product = self.get_object()
        # Mengizinkan akses hanya jika penjualnya adalah user yang sedang login
        return self.request.user == product.seller


# 5. VIEW HAPUS PRODUK - Menggunakan UserPassesTestMixin
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('seller_dashboard')

    def test_func(self):
        # Mengambil data objek produk yang diakses
        product = self.get_object()
        # Mengizinkan akses hanya jika penjualnya adalah user yang sedang login
        return self.request.user == product.seller