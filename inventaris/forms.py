from django import forms
from .models import Gitar


class GitarForm(forms.ModelForm):

  class Meta:
    model = Gitar
    fields = [
        'nama_gitar',
        'brand_model',
        'harga_beli',
        'biaya_tambahan',
        'tanggal_masuk',
    ]
    widgets = {
        'nama_gitar': forms.TextInput(attrs={'class': 'form-control'}),
        'brand_model': forms.TextInput(attrs={'class': 'form-control'}),
        'harga_beli': forms.NumberInput(
            attrs={'class': 'form-control', 'id': 'id_harga_beli'}
        ),
        'biaya_tambahan': forms.NumberInput(
            attrs={'class': 'form-control', 'id': 'id_biaya_tambahan'}
        ),
        'harga_jual': forms.NumberInput(attrs={'class': 'form-control'}),
        'tanggal_masuk': forms.DateInput(
            attrs={'class': 'form-control', 'type': 'date'}
        ),
    }
    
class JualGitarForm(forms.ModelForm):
  # Form khusus untuk mengisi harga jual saat barang laku

  class Meta:
    model = Gitar
    fields = ['harga_jual']
    widgets = {
        'harga_jual': forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Masukkan Harga Jual'}
        ),
    }