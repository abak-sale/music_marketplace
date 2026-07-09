from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class SignUpForm(forms.ModelForm):
    whatsapp_number = forms.CharField(
        max_length=20,
        label="Nomor WhatsApp Aktif",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contoh: 628123456789 (Gunakan kode negara tanpa tanda +)'
        })
    )
    password = forms.CharField(
        label="Kata Sandi",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Minimal 6 karakter'})
    )
    password_confirm = forms.CharField(
        label="Konfirmasi Kata Sandi",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ulangi kata sandi'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: abak_music'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: nama@email.com'}),
        }

    # Validasi nomor WhatsApp agar hanya berisi angka
    def clean_whatsapp_number(self):
        wa = self.cleaned_data.get('whatsapp_number').strip().replace('+', '').replace(' ', '')
        if not wa.isdigit():
            raise ValidationError("Nomor WhatsApp hanya boleh berisi angka saja!")
        if not wa.startswith('62'):
            raise ValidationError("Harap gunakan kode negara Indonesia (diawali dengan 62).")
        return wa

    # Validasi kecocokan password
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Kata sandi yang Anda masukkan tidak cocok!")
        return cleaned_data