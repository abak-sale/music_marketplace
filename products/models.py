from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Daftar Kategori"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nama Brand")
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Daftar Brand"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    CONDITION_CHOICES = [
        ('baru', 'Baru (Brand New)'),
        ('mulus', 'Bekas Mulus (Mint)'),
        ('bagus', 'Bekas Bagus (Good Condition)'),
        ('butuh_perbaikan', 'Butuh Perbaikan (Fair/Broken)'),
    ]

    # KITA TAMBAHKAN RELASI PENJUAL (USER) DI SINI
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Penjual"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='products',
        verbose_name="Kategori"
    )
    brand = models.ForeignKey(
        Brand, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='products',
        verbose_name="Brand"
    )
    name = models.CharField(max_length=255, verbose_name="Nama Alat Musik")
    description = models.TextField(verbose_name="Deskripsi Produk")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Harga (Rp)")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='baru', verbose_name="Kondisi")
    location = models.CharField(max_length=100, default='Batam', verbose_name="Lokasi Pengiriman")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Foto Utama (Cover)")
    is_sold = models.BooleanField(default=False, verbose_name="Sudah Terjual")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Produk"
        verbose_name_plural = "Daftar Produk"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Produk")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Foto Galeri")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foto Galeri"
        verbose_name_plural = "Galeri Foto Tambahan"

    def __str__(self):
        return f"Foto tambahan untuk {self.product.name}"