from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3 # Otomatis menyediakan 3 baris kosong siap upload foto tambahan
    max_num = 10 # Membatasi maksimal 10 foto per produk

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'condition', 'location', 'is_sold', 'created_at')
    list_filter = ('condition', 'is_sold', 'location')
    search_fields = ('name', 'description')
    
    # Memasukkan fungsi upload multi-foto ke dalam form produk
    inlines = [ProductImageInline]