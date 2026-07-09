from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Product
from .forms import ProductForm

# ==============================================================================
# 1. VIEW BERANDA / LIST PRODUK UTAMA (DENGAN FILTER KATEGORI)
# ==============================================================================
class HomeView(ListView):
    model = Product
    template_name = 'home.html' 
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        category_slug = self.request.GET.get('category', '')
        
        # Mulai dengan filter produk yang belum terjual
        queryset = Product.objects.filter(is_sold=False).order_by('-created_at')
        
        # Filter Pencarian Teks
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()
        
        # Filter Kategori
        if category_slug:
            queryset = queryset.filter(category__name__iexact=category_slug)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context

# ==============================================================================
# (Sisanya tetap sama: DetailView, SellerDashboardView, dsb...)
# ==============================================================================
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

class SellerDashboardView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/seller_dashboard.html'
    context_object_name = 'my_products'
    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('seller_dashboard')
    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'  
    success_url = reverse_lazy('seller_dashboard')
    def test_func(self):
        return self.request.user == self.get_object().seller

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('seller_dashboard')
    def test_func(self):
        return self.request.user == self.get_object().seller

def seller_profile_view(request, username):
    seller = get_object_or_404(User, username=username)
    seller_products = Product.objects.filter(seller=seller, is_sold=False).order_by('-created_at')
    return render(request, 'products/seller_profile.html', {'seller': seller, 'seller_products': seller_products})