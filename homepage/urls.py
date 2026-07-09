from django.urls import path
from .views import HomepageView, signup_view

urlpatterns = [
    # Rute Beranda Utama milik Om yang sudah ada sebelumnya
    path('', HomepageView.as_view(), name='home'),
    
    # Rute Baru untuk Pendaftaran Akun Penjual
    path('signup/', signup_view, name='signup'),
]