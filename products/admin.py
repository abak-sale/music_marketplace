from django.contrib import admin
from .models import Product, ProductImage, Category, Brand

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Tambahkan 'seller' ke dalam list_display dan list_filter
    list_display = ('name', 'seller', 'brand', 'category', 'price', 'condition', 'is_sold', 'created_at')
    list_filter = ('seller', 'brand', 'category', 'condition', 'is_sold', 'location')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]