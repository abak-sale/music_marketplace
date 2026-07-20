from django.db import models
from django.utils import timezone


class Gitar(models.Model):
  STATUS_CHOICES = [
      ('Tersedia', 'Tersedia'),
      ('Terjual', 'Terjual'),
  ]

  nama_gitar = models.CharField(max_length=150)
  brand_model = models.CharField(max_length=150)
  harga_beli = models.DecimalField(max_digits=12, decimal_places=2)
  biaya_tambahan = models.DecimalField(
      max_digits=12, decimal_places=2, default=0
  )
  total_modal = models.DecimalField(max_digits=12, decimal_places=2)
  harga_jual = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

  tanggal_masuk = models.DateField(default=timezone.now)
  tanggal_terjual = models.DateField(blank=True, null=True)

  status = models.CharField(
      max_length=20, choices=STATUS_CHOICES, default='Tersedia'
  )

  def save(self, *args, **kwargs):
    # Otomatis hitung total modal sebelum disimpan
    self.total_modal = self.harga_beli + self.biaya_tambahan
    super().save(*args, **kwargs)

  @property
  def laba(self):
    if self.status == 'Terjual' and self.harga_jual is not None:
      return self.harga_jual - self.total_modal
    return 0

  def __str__(self):
    return f'{self.brand_model} - {self.nama_gitar} ({self.status})'