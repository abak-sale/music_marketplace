from django import template

register = template.Library()

@register.filter(name='replace_commas')
def replace_commas(value):
    # Mengubah tanda koma separator internasional menjadi titik gaya Indonesia
    return str(value).replace(',', '.')