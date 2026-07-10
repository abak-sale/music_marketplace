from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from .utils import optimize_image


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

    def save(self, *args, **kwargs):
        # Cek apakah foto cover BARU saja diganti — supaya kita
        # tidak mengoptimasi ulang foto yang sudah pernah dioptimasi
        # sebelumnya (kalau dipaksa jalan setiap save, kualitas
        # gambar akan terus menurun tiap kali produk diedit,
        # meskipun fotonya tidak diganti sama sekali).
        is_new_image = False
        if self.pk:
            old = Product.objects.filter(pk=self.pk).first()
            if old and old.image != self.image:
                is_new_image = True
        else:
            is_new_image = bool(self.image)

        super().save(*args, **kwargs)

        if is_new_image and self.image:
            optimize_image(self.image)

    def get_image_url(self):
        if self.image:
            return self.image.url
        return ""


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Produk")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="Foto Galeri")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Foto Galeri"
        verbose_name_plural = "Galeri Foto Tambahan"

    def __str__(self):
        return f"Foto tambahan untuk {self.product.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            optimize_image(self.image)