from django.views.generic import TemplateView
from products.models import Product  # Impor model Product dari app products

class HomepageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        # Mengambil context bawaan dari TemplateView
        context = super().get_context_data(**kwargs)
        
        # Mengambil semua data produk dari database yang BELUM terjual
        # dan membatasi hanya muncul maksimal 8 produk terbaru di homepage
        context['latest_products'] = Product.objects.filter(is_sold=False)[:8]
        
        return context