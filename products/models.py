from django.db import models

class Product(models.Model):
    # Pilihan kondisi alat musik (Sesuai gaya Reverb)
    CONDITION_CHOICES = [
        ('baru', 'Baru (Brand New)'),
        ('mulus', 'Bekas Mulus (Mint)'),
        ('bagus', 'Bekas Bagus (Good Condition)'),
        ('butuh_perbaikan', 'Butuh Perbaikan (Fair/Broken)'),
    ]

    name = models.CharField(max_length=255, verbose_name="Nama Alat Musik")
    description = models.TextField(verbose_name="Deskripsi Produk")
    
    # PERBAIKAN: Mengubah decimal_digits menjadi decimal_places
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Harga (Rp)")
    
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='baru', verbose_name="Kondisi")
    location = models.CharField(max_length=100, default='Batam', verbose_name="Lokasi Pengiriman")
    is_sold = models.BooleanField(default=False, verbose_name="Sudah Terjual")
    
    # Catatan waktu otomatis saat produk dibuat dan diperbarui
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Mengurutkan produk berdasarkan yang terbaru diunggah
        ordering = ['-created_at']
        verbose_name = "Produk"
        verbose_name_plural = "Daftar Produk"

    def __str__(self):
        # Menentukan teks apa yang muncul saat data ini dipanggil (misal di halaman Admin)
        return self.name