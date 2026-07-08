from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Kolom apa saja yang mau kita tampilkan di tabel panel admin
    list_display = ('name', 'price', 'condition', 'location', 'is_sold', 'created_at')
    # Filter cepat di bagian kanan panel admin
    list_filter = ('condition', 'is_sold', 'location')
    # Fitur pencarian produk berdasarkan nama
    search_fields = ('name', 'description')