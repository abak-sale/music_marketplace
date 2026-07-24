from django.urls import path
from .views import HomepageView, signup_view, verify_email_view

urlpatterns = [
    # Rute Beranda Utama
    path('', HomepageView.as_view(), name='home'),

    # Rute Pendaftaran Akun Penjual
    path('signup/', signup_view, name='signup'),

    # Rute Verifikasi Email
    path('verify-email/<uidb64>/<token>/', verify_email_view, name='verify_email'),
]