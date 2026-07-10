from django import forms
from .models import Product


class MultipleFileInput(forms.ClearableFileInput):
    """
    Widget bawaan Django (ClearableFileInput) secara default
    hanya izinkan 1 file. Kita 'nyalakan' atribut HTML
    'multiple' supaya browser mengizinkan user pilih banyak file.
    """
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    """
    FileField bawaan Django hanya tahu cara membersihkan (clean)
    SATU file. Di sini kita override supaya bisa membersihkan
    LIST file sekaligus — masing-masing tetap divalidasi
    satu per satu pakai logic FileField asli.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ProductForm(forms.ModelForm):
    # Field TAMBAHAN — TIDAK ada di Model Product, murni untuk
    # menampung upload banyak file sekaligus ke ProductImage nanti
    extra_images = MultipleFileField(
        required=False,
        label="Foto Tambahan (Maks. 10 foto)",
        widget=MultipleFileInput(attrs={
            "class": "form-control",
            "accept": "image/*",
        }),
    )

    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'price', 'condition', 'location', 'image', 'description']

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

    def clean_extra_images(self):
        """
        Validasi maksimal 10 foto SAAT membuat produk baru.
        (Untuk halaman EDIT, batasan dihitung ulang di views.py
        karena perlu tahu jumlah foto yang sudah ada dulu.)
        """
        files = self.cleaned_data.get("extra_images")
        if files and len(files) > 10:
            raise forms.ValidationError(
                f"Maksimal 10 foto tambahan. Kamu memilih {len(files)} foto."
            )
        return files