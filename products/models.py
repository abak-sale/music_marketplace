from django.db import models

class Product(models.Model):
    CONDITION_CHOICES = [
        ('baru', 'Baru (Brand New)'),
        ('mulus', 'Bekas Mulus (Mint)'),
        ('bagus', 'Bekas Bagus (Good Condition)'),
        ('butuh_perbaikan', 'Butuh Perbaikan (Fair/Broken)'),
    ]

    name = models.CharField(max_length=255, verbose_name="Nama Alat Musik")
    description = models.TextField(verbose_name="Deskripsi Produk")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Harga (Rp)")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='baru', verbose_name="Kondisi")
    location = models.CharField(max_length=100, default='Batam', verbose_name="Lokasi Pengiriman")
    
    # BARU: Kolom untuk menyimpan gambar produk (boleh kosong dulu dengan blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Foto Produk")
    
    is_sold = models.BooleanField(default=False, verbose_name="Sudah Terjual")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Produk"
        verbose_name_plural = "Daftar Produk"

    def __str__(self):
        return self.name