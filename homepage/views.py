from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login
from products.models import Product  # Impor model Product dari app products
from .forms import SignUpForm
from products.views import HomeView
# 1. VIEW BERANDA UTAMA (Milik Anda yang asli)
class HomepageView(HomeView):
    pass
    
    def get_context_data(self, **kwargs):
        # Mengambil context bawaan dari TemplateView
        context = super().get_context_data(**kwargs)
        
        # Mengambil semua data produk dari database yang BELUM terjual
        # dan membatasi hanya muncul maksimal 8 produk terbaru di homepage
        context['latest_products'] = Product.objects.filter(is_sold=False)[:8]
        
        return context


# 2. VIEW PENDAFTARAN AKUN BARU (Tambahan Fitur Registrasi)
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Jika sudah login, dilempar ke beranda utama
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Mengamankan kata sandi dengan enkripsi Django
            user.set_password(form.cleaned_data['password'])
            # Menyimpan nomor WA ke field first_name agar terbaca otomatis oleh tombol chat WA
            user.first_name = form.cleaned_data['whatsapp_number']
            user.save()
            
            # Otomatis login setelah berhasil mendaftar
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
        
    return render(request, 'homepage/signup.html', {'form': form})