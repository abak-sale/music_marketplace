from django import template
from products.models import Product  # Pastikan import model-nya benar

register = template.Library()

@register.filter(name='replace_commas')
def replace_commas(value):
    # Mengubah tanda koma separator internasional menjadi titik gaya Indonesia
    return str(value).replace(',', '.')

@register.simple_tag
def get_categories():
    # Mengambil daftar kategori unik dari database
    return Product.objects.values_list('category__name', flat=True).distinct().order_by('category__name')