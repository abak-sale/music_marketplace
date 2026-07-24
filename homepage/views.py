from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from products.models import Product
from .forms import SignUpForm
from products.views import HomeView


# 1. VIEW BERANDA UTAMA (Milik Anda yang asli)
class HomepageView(HomeView):
    pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products'] = Product.objects.filter(is_sold=False)[:8]
        return context


# 2. VIEW PENDAFTARAN AKUN BARU
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['whatsapp_number']

            # Akun BELUM aktif sampai email diverifikasi!
            user.is_active = False
            user.save()

            kirim_email_verifikasi(request, user)

            return render(request, 'homepage/verify_email_sent.html', {
                'email': user.email
            })
    else:
        form = SignUpForm()

    return render(request, 'homepage/signup.html', {'form': form})


# 3. FUNGSI HELPER — KIRIM EMAIL VERIFIKASI
def kirim_email_verifikasi(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    verification_link = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )

    subject = 'Verifikasi Email Akun Abak Sale'
    message = render_to_string('homepage/verification_email.html', {
        'user': user,
        'verification_link': verification_link,
    })

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])


# 4. VIEW UNTUK PROSES VERIFIKASI (saat link diklik)
def verify_email_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'homepage/verify_email_success.html')
    else:
        return render(request, 'homepage/verify_email_invalid.html')