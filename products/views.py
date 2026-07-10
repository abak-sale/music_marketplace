from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from .models import Product, ProductImage
from .forms import ProductForm

# ==============================================================================
# 1. VIEW BERANDA / LIST PRODUK UTAMA (DENGAN FILTER KATEGORI & KONDISI)
# ==============================================================================
class HomeView(ListView):
    model = Product
    template_name = 'home.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        category_slug = self.request.GET.get('category', '')
        condition_slug = self.request.GET.get('condition', '')

        queryset = Product.objects.filter(is_sold=False).order_by('-created_at')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(category__name__icontains=query)
            ).distinct()

        if category_slug:
            queryset = queryset.filter(category__name__iexact=category_slug)

        if condition_slug:
            queryset = queryset.filter(condition__iexact=condition_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_condition'] = self.request.GET.get('condition', '')
        return context


# ==============================================================================
# 2. VIEW DETAIL PRODUK
# ==============================================================================
class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'


# ==============================================================================
# 3. VIEW DASHBOARD PENJUAL (DASHBOARD SAYA)
# ==============================================================================
class SellerDashboardView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/seller_dashboard.html'
    context_object_name = 'my_products'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')


# ==============================================================================
# 4. VIEW TAMBAH PRODUK
# ==============================================================================
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('seller_dashboard')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        response = super().form_valid(form)

        # self.object sudah terisi Product yang baru saja disimpan
        # (otomatis diisi CreateView setelah form.save() dipanggil)
        extra_images = form.cleaned_data.get('extra_images')
        if extra_images:
            for img_file in extra_images:
                ProductImage.objects.create(
                    product=self.object,
                    image=img_file
                )
            messages.success(
                self.request,
                f"Produk berhasil ditambahkan dengan {len(extra_images)} foto tambahan."
            )
        else:
            messages.success(self.request, "Produk berhasil ditambahkan.")

        return response


# ==============================================================================
# 5. VIEW EDIT PRODUK
# ==============================================================================
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('seller_dashboard')

    def test_func(self):
        return self.request.user == self.get_object().seller

    def form_valid(self, form):
        response = super().form_valid(form)

        extra_images = form.cleaned_data.get('extra_images')
        if extra_images:
            # Hitung foto yang SUDAH ADA + foto BARU yang mau ditambahkan
            jumlah_foto_lama = self.object.images.count()
            total_setelah_upload = jumlah_foto_lama + len(extra_images)

            if total_setelah_upload > 10:
                sisa_slot = 10 - jumlah_foto_lama
                messages.warning(
                    self.request,
                    f"Produk ini sudah punya {jumlah_foto_lama} foto tambahan. "
                    f"Hanya {sisa_slot} foto pertama yang disimpan (maksimal 10 foto)."
                )
                extra_images = extra_images[:sisa_slot] if sisa_slot > 0 else []

            for img_file in extra_images:
                ProductImage.objects.create(
                    product=self.object,
                    image=img_file
                )

        messages.success(self.request, "Produk berhasil diperbarui.")
        return response


# ==============================================================================
# 6. VIEW HAPUS PRODUK
# ==============================================================================
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('seller_dashboard')

    def test_func(self):
        return self.request.user == self.get_object().seller


# ==============================================================================
# 7. VIEW PROFIL PENJUAL
# ==============================================================================
def seller_profile_view(request, username):
    seller = get_object_or_404(User, username=username)
    seller_products = Product.objects.filter(seller=seller, is_sold=False).order_by('-created_at')
    return render(request, 'products/seller_profile.html', {'seller': seller, 'seller_products': seller_products})