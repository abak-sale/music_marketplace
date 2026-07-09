from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Field yang diizinkan untuk diisi oleh penjual di halaman depan
        fields = ['name', 'category', 'brand', 'price', 'condition', 'location', 'image', 'description']
        
        # Memberikan style bootstrap otomatis pada setiap kolom input
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Fender Stratocaster 2012'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nominal tanpa titik (Contoh: 5000000)'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: Batam'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Jelaskan spesifikasi, minus, atau kelengkapan alat musik...'}),
        }